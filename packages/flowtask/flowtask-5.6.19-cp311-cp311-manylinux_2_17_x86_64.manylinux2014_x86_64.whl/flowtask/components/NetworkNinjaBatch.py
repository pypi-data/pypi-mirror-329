import asyncio
from collections.abc import Callable
import pandas as pd
from ..interfaces.http import HTTPService
from .flow import FlowComponent
from ..exceptions import ComponentError, DataNotFound
from ..conf import NETWORKNINJA_API_KEY, NETWORKNINJA_BASE_URL

class NetworkNinjaBatch(HTTPService, FlowComponent):
    """
    NetworkNinjaBatch Component

    Overview:
        This component makes API calls to Network Ninja's batch endpoints.

    Properties:
        +---------------+----------+------------------------------------------+
        | Name          | Required | Description                              |
        +---------------+----------+------------------------------------------+
        | type          | Yes      | Type of operation (get_batch, etc)      |
        +---------------+----------+------------------------------------------+
        | credentials   | No       | API credentials (taken from config)      |
        +---------------+----------+------------------------------------------+
        | payload       | No       | Additional payload parameters            |
        +---------------+----------+------------------------------------------+

    Supported Types:
        - get_batch: Retrieves batch acceptance data
        (Future types can be added here)

    Returns:
        pandas.DataFrame: The response data from the API
    """

    accept = "application/json"
    
    # Mapping of types to endpoints
    ENDPOINTS = {
        "get_batch": "/acceptance/get_batch",
        # Add more endpoints here as needed
    }

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs
    ):
        self.type = kwargs.get('type', 'get_batch')
        self.payload = kwargs.get('payload', {})
        
        if self.type not in self.ENDPOINTS:
            raise ComponentError(f"Unsupported operation type: {self.type}")
        
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Initialize the component and set up headers"""
        # Validate and set up API key
        if not NETWORKNINJA_API_KEY:
            raise ComponentError("NETWORKNINJA_API_KEY not found in configuration")

        # Validate and set up base URL
        if not NETWORKNINJA_BASE_URL:
            raise ComponentError("NETWORKNINJA_BASE_URL not found in configuration")
        self.base_url = NETWORKNINJA_BASE_URL

        # Set up headers with API key
        self.headers.update({
            "X-Api-Key": NETWORKNINJA_API_KEY
        })

        if self.previous:
            self.data = self.input

        return await super().start(**kwargs)

    async def get_batch(self):
        """Handle get_batch operation type"""
        url = f"{self.base_url}{self.ENDPOINTS['get_batch']}"
        
        args = {
            "method": "get",
            "url": url,
            "use_proxy": False
        }

        result, error = await self.session(**args)

        if error:
            raise ComponentError(f"Error calling Network Ninja API: {error}")

        if not result:
            raise DataNotFound("No data returned from Network Ninja API")

        return result

    async def run(self):
        """Execute the API call to Network Ninja based on type"""
        try:
            # Get the appropriate method for the type
            method = getattr(self, self.type, None)
            if not method:
                raise ComponentError(f"Method not implemented for type: {self.type}")

            # Execute the method
            result = await method()

            # Convert result to DataFrame if it's not already
            if not isinstance(result, pd.DataFrame):
                df = await self.create_dataframe(result)
            else:
                df = result

            # Add metrics
            self.add_metric("TYPE", self.type)
            self.add_metric("ROWS", len(df.index))
            self.add_metric("COLUMNS", len(df.columns))

            if self._debug:
                self._print_data_(df, f"Network Ninja {self.type} Data")

            self._result = df
            return self._result

        except Exception as e:
            raise ComponentError(f"Error in NetworkNinjaBatch ({self.type}): {str(e)}") from e

    async def close(self):
        """Clean up any resources"""
        return True 