from pydantic import BaseModel
from typing import Union, Dict, Any, Optional
from functools import cached_property
from ethereal.constants import API_PREFIX
from ethereal.rest.http_client import HTTPClient
from ethereal.chain_client import ChainClient
from ethereal.models.config import RESTConfig, ChainConfig
from ethereal.models.rest import (
    TimeInForce,
    RpcConfigDto,
)


class RESTClient(HTTPClient):
    """REST client for interacting with the Ethereal API.

    Args:
        config (Union[Dict[str, Any], RESTConfig]): Configuration dictionary or RESTConfig object.
            Optional fields include:
            - private_key (str): The private key
            - base_url (str): Base URL for REST requests, defaults to "https://api.etherealtest.net"
            - timeout (int): Timeout in seconds for REST requests
            - verbose (bool): Enables debug logging, defaults to False
            - rate_limit_headers (bool): Enables rate limit headers, defaults to False
    """

    from ethereal.rest.funding import list_funding_rates
    from ethereal.rest.linked_signer import (
        get_active_signer,
        get_signer,
        get_signer_quota,
        list_signers,
        link_signer,
    )
    from ethereal.rest.order import (
        get_order,
        list_fills,
        list_orders,
        list_trades,
        submit_order as _submit_order,
        cancel_order,
    )
    from ethereal.rest.position import list_positions, get_position
    from ethereal.rest.product import (
        get_market_liquidity,
        list_market_prices,
        list_products,
    )
    from ethereal.rest.rpc import get_rpc_config
    from ethereal.rest.subaccount import (
        list_subaccounts,
        get_subaccount,
        get_subaccount_balances,
    )
    from ethereal.rest.token import (
        get_token,
        list_token_withdraws,
        list_tokens,
        list_token_transfers,
        withdraw_token,
    )

    def __init__(self, config: Union[Dict[str, Any], RESTConfig] = {}):
        super().__init__(config)
        self.config = RESTConfig.model_validate(config)

        # fetch RPC configuration
        self.rpc_config = self.get_rpc_config()

        self.chain = None
        if self.config.chain_config:
            self._init_chain_client(self.config.chain_config, self.rpc_config)
            self.private_key = self.chain.private_key
            self.provider = self.chain.provider
        else:
            self.private_key = None
            self.provider = None

        # TODO: Find a better way to set these default
        self.default_time_in_force = TimeInForce.IOC
        self.default_post_only = False

    def _init_chain_client(
        self,
        config: Union[Dict[str, Any], ChainConfig],
        rpc_config: RpcConfigDto = None,
    ):
        """Initialize the ChainClient.

        Args:
            config (Union[Dict[str, Any], ChainConfig]): The chain configuration.
            rpc_config (RpcConfigDto, optional): RPC configuration. Defaults to None.
        """
        config = ChainConfig.model_validate(config)
        try:
            self.chain = ChainClient(config, rpc_config)
            self.logger.info("Chain client initialized successfully")
        except Exception as e:
            self.logger.warning(f"Failed to initialize chain client: {e}")

    def _get_pages(
        self,
        endpoint: str,
        request_model: BaseModel,
        response_model: BaseModel,
        paginate: bool = False,
        **kwargs,
    ) -> BaseModel:
        """Make a GET request with validated parameters and response and handling for pagination.

        Args:
            endpoint (str): API endpoint path (e.g. "order" will be appended to the base URL and prefix to form "/v1/order")
            request_model (BaseModel): Pydantic model for request validation
            response_model (BaseModel): Pydantic model for response validation
            paginate (bool): Whether to fetch additional pages of data
            **kwargs: Parameters to validate and include in the request

        Returns:
            response (BaseModel): Validated response object

        Example:
            orders = client.validated_get(
                endpoint="order",
                request_model=V1OrderGetParametersQuery,
                response_model=ListOfOrderDtos,
                subaccountId="abc123",
                limit=50
            )
        """
        result = self.get_validated(
            url_path=f"{API_PREFIX}/{endpoint}",
            request_model=request_model,
            response_model=response_model,
            **kwargs,
        )

        # If pagination is requested, fetch additional pages
        is_paginated = all(
            [
                hasattr(result, "data"),
                hasattr(result, "hasNext"),
                hasattr(result, "nextCursor"),
            ]
        )
        if not is_paginated:
            raise ValueError("Response does not support pagination")
        elif paginate:
            all_data = list(result.data)

            # Continue fetching while there are more pages
            current_result = result
            while current_result.hasNext and current_result.nextCursor:
                current_result = self.get_validated(
                    url_path=f"{API_PREFIX}/{endpoint}",
                    request_model=request_model,
                    response_model=response_model,
                    cursor=current_result.nextCursor,
                    **kwargs,
                )
                # Add data from this page
                all_data.extend(current_result.data)

            # Update the result with the combined data
            result.data = all_data
            result.hasNext = False
            result.nextCursor = None
        return result.data

    @cached_property
    def subaccounts(self):
        """Get the list of subaccounts.

        Returns:
            subaccounts (List): List of subaccount objects.
        """
        return self.list_subaccounts(self.chain.address)

    @cached_property
    def products(self):
        """Get the list of products.

        Returns:
            products (List): List of product objects.
        """
        return self.list_products()

    @cached_property
    def products_by_ticker(self):
        """Get the products indexed by ticker.

        Returns:
            products_by_ticker (Dict[str, ProductDto]): Dictionary of products keyed by ticker.
        """
        return {p.ticker: p for p in self.products}

    @cached_property
    def products_by_id(self):
        """Get the products indexed by ID.

        Returns:
            products_by_id (Dict[str, ProductDto]): Dictionary of products keyed by ID.
        """
        return {p.id: p for p in self.products}

    def create_order(
        self,
        order_type: str,
        quantity: float,
        side: int,
        price: Optional[float] = None,
        ticker: Optional[str] = None,
        product_id: Optional[str] = None,
        sender: Optional[str] = None,
        subaccount: Optional[str] = None,
        time_in_force: Optional[str] = None,
        post_only: Optional[bool] = None,
    ):
        """Create and submit an order.

        Args:
            order_type (str): The type of order (market or limit)
            quantity (float): The quantity of the order
            side (int): The side of the order (0 = BUY, 1 = SELL)
            price (float, optional): The price of the order (for limit orders)
            ticker (str, optional): The ticker of the product
            product_id (str, optional): The ID of the product
            sender (str, optional): The sender address
            subaccount (str, optional): The subaccount name
            time_in_force (str, optional): The time in force for limit orders
            post_only (bool, optional): Whether the order is post-only (for limit orders)

        Returns:
            order (OrderDto): The response data from the API

        Raises:
            ValueError: If neither product_id nor ticker is provided or if order type is invalid
        """
        # get the sender and account info
        if sender is None:
            sender = self.chain.address
        if subaccount is None:
            subaccount = self.subaccounts[0].name

        # get the product info
        if product_id is not None:
            onchain_id = self.products_by_id[product_id].onchainId
        elif ticker is not None:
            onchain_id = self.products_by_ticker[ticker].onchainId
        else:
            raise ValueError("Either product_id or ticker must be provided")

        # prepare the order params
        quantity = str(quantity)
        if order_type == "MARKET":
            order_params = {
                "sender": sender,
                "subaccount": subaccount,
                "side": side,
                "price": "0",
                "quantity": quantity,
                "onchainId": onchain_id,
                "orderType": order_type,
            }
        elif order_type == "LIMIT":
            time_in_force = (
                self.default_time_in_force if time_in_force is None else time_in_force
            )
            post_only = self.default_post_only if post_only is None else post_only
            price = "{:.9f}".format(price)

            order_params = {
                "sender": sender,
                "subaccount": subaccount,
                "side": side,
                "price": price,
                "quantity": quantity,
                "onchainId": onchain_id,
                "orderType": order_type,
                "timeInForce": time_in_force,
                "postOnly": post_only,
            }
        else:
            raise ValueError("Invalid order type")

        return self._submit_order(**order_params)
