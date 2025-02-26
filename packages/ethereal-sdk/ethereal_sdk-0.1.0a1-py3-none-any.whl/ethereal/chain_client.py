import os
import json

from typing import Optional, Dict, Any, Union
from ethereal.base_client import BaseClient
from ethereal.models.config import ChainConfig
from ethereal.models.rest import RpcConfigDto
from web3 import Web3
from web3.exceptions import Web3Exception
from web3.types import TxParams
from eth_account import Account
from eth_account.messages import encode_typed_data
from eth_utils import encode_hex


# constants
USDE_ADDRESSES = {996353: "0xa1623E0AA40B142Cf755938b325321fB2c61Cf05"}


def read_contract(contract_name: str):
    contract_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "contracts",
        f"{contract_name}.json",
    )
    with open(contract_dir) as f:
        return json.load(f)


class ChainClient(BaseClient):
    """Client for interacting with the blockchain using Web3 functionality.

    Args:
        config (Union[Dict[str, Any], ChainConfig]): Chain configuration
        rpc_config (RpcConfigDto, optional): RPC configuration. Defaults to None.

    Raises:
        Exception: If RPC URL or private key is not specified in the configuration
    """

    def __init__(
        self,
        config: Union[Dict[str, Any], ChainConfig],
        rpc_config: RpcConfigDto = None,
    ):
        super().__init__(config)
        self.config = ChainConfig.model_validate(config)
        self.provider = self._setup_provider()
        self.account = self._setup_account()
        self.address = self.account.address
        self.private_key = self.config.private_key

        self.chain_id = self.provider.eth.chain_id
        self.usde = self.provider.eth.contract(
            address=USDE_ADDRESSES[self.chain_id], abi=read_contract("ERC20")
        )
        self.rpc_config = rpc_config

    def _setup_provider(self):
        """Set up the Web3 provider.

        Returns:
            Web3: The Web3 provider instance

        Raises:
            Exception: If RPC URL is not specified in the configuration
        """
        # TODO: Support other provider types (e.g. WebSocket)
        if self.config.rpc_url is None:
            raise Exception("RPC URL must be specified in the configuration")
        return Web3(Web3.HTTPProvider(self.config.rpc_url))

    def _setup_account(self):
        """Set up the account.

        Returns:
            Account: The Web3 account instance

        Raises:
            Exception: If private key is not specified in the configuration
        """
        if self.config.private_key is None:
            raise Exception("Private key must be specified in the configuration")
        return self.provider.eth.account.from_key(self.config.private_key)

    def _get_tx(self, value=0, to=None) -> TxParams:
        """Get default transaction parameters.

        Args:
            value (int, optional): The value to send. Defaults to 0.
            to (str, optional): The recipient address. Defaults to None.

        Returns:
            TxParams: The transaction parameters
        """
        params: TxParams = {
            "from": self.address,
            "chainId": self.chain_id,
            "value": value,
            "nonce": self.get_nonce(self.address),
        }
        if to is not None:
            params["to"] = to
        return params

    def add_gas_fees(self, tx: TxParams) -> TxParams:
        """Add gas fee parameters to a transaction.

        Args:
            tx (TxParams): The transaction parameters

        Returns:
            TxParams: The transaction parameters with gas fee parameters added
        """
        if "maxFeePerGas" in tx and "maxPriorityFeePerGas" in tx:
            return tx
        try:
            gas_price = self.provider.eth.gas_price
            max_priority_fee = self.provider.eth.max_priority_fee
            tx["maxFeePerGas"] = gas_price
            tx["maxPriorityFeePerGas"] = max_priority_fee
            return tx
        except Web3Exception as e:
            self.logger.error(f"Failed to add gas: {e}")
            return tx

    def add_gas_limit(self, tx: TxParams) -> TxParams:
        """Add gas limit to a transaction.

        Args:
            tx (TxParams): The transaction parameters

        Returns:
            TxParams: The transaction parameters with gas limit added
        """
        if "gas" in tx:
            return tx
        try:
            gas = self.provider.eth.estimate_gas(tx)
            tx["gas"] = gas
            return tx
        except Web3Exception as e:
            self.logger.error(f"Failed to add gas limit: {e}")
            return

    def submit_tx(self, tx: TxParams) -> str:
        """Submit a transaction.

        Args:
            tx (TxParams): The transaction parameters

        Returns:
            str: The transaction hash
        """
        tx = self.add_gas_fees(tx)
        tx = self.add_gas_limit(tx)
        try:
            signed_tx = self.provider.eth.account.sign_transaction(
                tx, private_key=self.private_key
            )
            tx_hash = self.provider.eth.send_raw_transaction(signed_tx.raw_transaction)
            return encode_hex(tx_hash)
        except Web3Exception as e:
            self.logger.error(f"Failed to submit transaction: {e}")
            return

    def get_nonce(self, address: str) -> int:
        """Get the nonce for a given address.

        Args:
            address (str): The address to get the nonce for

        Returns:
            int: The nonce, or -1 if failed
        """
        try:
            return self.provider.eth.get_transaction_count(address)
        except Web3Exception as e:
            self.logger.error(f"Failed to get nonce: {e}")
            return -1

    def get_balance(self, address: str) -> int:
        """Get the balance for a given address.

        Args:
            address (str): The address to get the balance for

        Returns:
            int: The balance, or -1 if failed
        """
        try:
            return self.provider.eth.get_balance(address)
        except Web3Exception as e:
            self.logger.error(f"Failed to get balance: {e}")
            return -1

    def get_token_balance(self, address: str, token_address: str) -> int:
        """Get the token balance for a given address.

        Args:
            address (str): The address to get the token balance for
            token_address (str): The token address

        Returns:
            int: The token balance, or -1 if failed
        """
        try:
            contract = self.provider.eth.contract(
                address=token_address, abi=read_contract("ERC20")
            )
            return contract.functions.balanceOf(address).call()
        except Web3Exception as e:
            self.logger.error(f"Failed to get token balance: {e}")
            return -1

    def sign_message(self, private_key, domain, types, primary_type, message):
        # A type fix for the domain
        domain["chainId"] = int(domain["chainId"])

        # Preparing the full message as per EIP-712
        full_message = {
            "types": types,
            "primaryType": primary_type,
            "domain": domain,
            "message": message,
        }

        encoded_message = encode_typed_data(full_message=full_message)

        # Signing the message
        signed_message = Account.sign_message(encoded_message, private_key)
        return "0x" + signed_message.signature.hex()

    def deposit_usde(
        self,
        amount: float,
        address: Optional[str] = None,
        submit: Optional[bool] = False,
        account_name: Optional[str] = "primary",
    ) -> Union[TxParams, str]:
        """Submit a deposit transaction.

        Args:
            amount (float): The amount to deposit
            address (str, optional): The address to deposit to. Defaults to None.
            submit (bool, optional): Whether to submit the transaction. Defaults to False.

        Returns:
            Union[TxParams, str]: The transaction parameters or transaction hash if submit=True
        """
        if address is None:
            address = self.address
        try:
            contract_address = self.rpc_config.domain.verifyingContract
            contract = self.provider.eth.contract(
                address=contract_address, abi=read_contract("EtherealProxy")
            )

            # params
            subaccount = self.provider.to_hex(text=account_name).ljust(66, "0")
            deposit_token = self.usde.address
            amount = self.provider.to_wei(amount, "ether")
            referral_code = self.provider.to_hex(0).ljust(66, "0")

            # prepare the tx
            tx = self._get_tx(to=contract_address)
            tx["data"] = contract.encode_abi(
                "deposit", args=[subaccount, deposit_token, amount, referral_code]
            )

            if submit:
                return self.submit_tx(tx)
            else:
                return tx

        except Web3Exception as e:
            self.logger.error(f"Failed to get token balance: {e}")
            return -1
