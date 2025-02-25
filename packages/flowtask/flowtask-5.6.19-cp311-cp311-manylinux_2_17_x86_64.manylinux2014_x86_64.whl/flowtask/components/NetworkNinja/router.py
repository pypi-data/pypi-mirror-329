from collections.abc import Callable
import asyncio
import pandas as pd
import backoff
from datamodel.exceptions import ValidationError
from ...exceptions import (
    ComponentError,
    DataError,
    ConfigError,
    DataNotFound
)
from ...components import FlowComponent
from ...utils.json import json_encoder
from ...interfaces.http import HTTPService
from ...conf import (
    NETWORKNINJA_API_KEY,
    NETWORKNINJA_BASE_URL
)
from .models import NetworkNinja_Map


class NetworkNinja(HTTPService, FlowComponent):
    """
    NetworkNinja.

        Overview: Router for processing NetworkNinja Payloads.
    """
    # Mapping of types to endpoints
    ENDPOINTS = {
        "get_batch": "/acceptance/get_batch",
    }

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        self.chunk_size: int = kwargs.get('chunk_size', 100)
        self._action: str = kwargs.pop('action', None)
        self.use_proxies: bool = kwargs.pop('use_proxies', False)
        self.paid_proxy: bool = kwargs.pop('paid_proxy', False)
        super(NetworkNinja, self).__init__(loop=loop, job=job, stat=stat, **kwargs)
        self.semaphore = asyncio.Semaphore(10)  # Adjust the limit as needed
        self._result: dict = {}
        self.accept = 'application/json'

    async def close(self):
        pass

    def _evaluate_input(self):
        if self.previous or self.input is not None:
            self.data = self.input

    def chunkify(self, lst, n):
        """Split list lst into chunks of size n."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    async def start(self, **kwargs):
        self._counter: int = 0
        self._evaluate_input()
        if not self._action:
            raise RuntimeError(
                'NetworkNinja component requires a *action* Function'
            )
        if self._action == 'download_batch':
            # Calling Download Batch from NN Queue.
            self.base_url = NETWORKNINJA_BASE_URL
            # Set up headers with API key
            self.headers.update({
                "X-Api-Key": NETWORKNINJA_API_KEY
            })
            return await super(NetworkNinja, self).start(**kwargs)
        # in other cases, NN requires a previous dataset downloaded.
        if not isinstance(self.data, dict):
            raise ComponentError(
                "NetworkNinja requires a Dictionary as Payload",
                status=404
            )
        return True

    async def run(self):
        """Run NetworkNinja Router."""
        tasks = []
        fn = getattr(self, self._action)
        self.add_metric("ACTION", self._action)
        self._result = {}
        if self._action == 'download_batch':
            result = await fn()

            # Check Length of the Payload:
            try:
                num_elements = len(result.get('data', []))
            except TypeError:
                num_elements = 0

            # Add metrics
            self.add_metric("PAYLOAD_LENGTH", num_elements)

            self._result = result
            return self._result
        if isinstance(self.data, dict):
            # Typical NN payload extract data from dictionary:
            tasks = [
                fn(
                    idx,
                    row,
                ) for idx, row in enumerate(self.data.get('data', []))
            ]
        elif isinstance(self.data, pd.DataFrame):
            tasks = [
                fn(
                    idx,
                    row,
                ) for idx, row in self.data.iterrows()
            ]
        # Execute tasks concurrently
        await self._processing_tasks(tasks)
        # taking actions based on data:
        if self._action == 'process_payload':
            for data_type, data in self._result.items():
                table_name = data_type
                await self.saving_payload(table_name, data)
        return self._result

    async def _processing_tasks(self, tasks: list) -> pd.DataFrame:
        """Process tasks concurrently."""
        results = []
        for chunk in self.chunkify(tasks, self.chunk_size):
            result = await asyncio.gather(*chunk, return_exceptions=True)
            if result:
                results.extend(result)
        return results

    @backoff.on_exception(
        backoff.expo,
        (asyncio.TimeoutError),
        max_tries=2
    )
    async def process_payload(
        self,
        idx,
        row
    ):
        async with self.semaphore:
            # Processing first the Metadata:
            metadata = row.get('metadata', {})
            payload = row.get('payload', {})
            # Client and Organization Information:
            client = metadata.get('client', None)
            payload_time = metadata.get('timestamp')
            # Data Type:
            data_type = metadata.get('type', None)
            if not data_type:
                raise DataError(
                    "NetworkNinja: Data Type not found in Metadata"
                )
            if data_type not in self._result:
                self._result[data_type] = []
            # Get the Model for the Data Type
            mdl = NetworkNinja_Map.get(data_type)
            if not mdl:
                raise DataError(
                    f"NetworkNinja: Model not found for Data Type: {data_type}"
                )
            error = None
            try:
                # First: adding client to payload:
                payload['client'] = client
                payload['payload_time'] = payload_time
                # Validate the Data
                data = mdl(**dict(payload))
                self._result[data_type].append(data)
                return data, error
            except ValidationError as e:
                self._logger.warning('Error: ==== ', e)
                error = e.payload
                self._logger.warning(
                    f'Validation Errors: {e.payload}'
                )
                # TODO: save bad payload to DB
                return None, error
            except Exception as e:
                print(f'Error: {e}')
                error = str(e)
                return None, error

    @backoff.on_exception(
        backoff.expo,
        (asyncio.TimeoutError),
        max_tries=2
    )
    async def saving_payload(
        self,
        tablename: str,
        data: list[dict]
    ):
        async with self.semaphore:
            # Iterate over all keys in data:
            custom_fields = {}
            if not data:
                return
            # extracting the fields and columns from first element:
            columns = data[0].get_fields()  # column names
            fields = data[0].columns().items()  # dataclass fields
            # Extracting primary keys:
            try:
                pk = [f for f in fields if f[1].primary_key is True]
            except IndexError:
                pk = []
            for item in data:
                # get column names from item:
                if item.client == 'global':
                    item.client = 'nn'
                item.Meta.schema = item.client
                # Convert to Dict:
                ds = item.to_dict()
                ## if item.has_column('custom_fields'):  # When new release of DataModel is available
                if 'custom_fields' in columns:
                    # Processing the Custom Fields (if any)
                    for custom in item.custom_fields:
                        # adding the PK to the custom Field Object:
                        for f, _ in pk:
                            # extracting FK from Parent PK
                            setattr(custom, f, getattr(item, f))
                        print(custom)
                        if custom.column_name not in columns:
                            # Avoid overriding existing columns:
                            custom_fields.update(
                                custom.get_field()
                            )
                    # removing the custom_fields:
                    ds.pop('custom_fields')
                    ds.update(custom_fields)
                print('Saving Data: ', ds)

    async def download_batch(self):
        """Handle get_batch operation type"""
        url = f"{self.base_url}{self.ENDPOINTS['get_batch']}"

        args = {
            "method": "get",
            "url": url,
            "use_proxy": False
        }

        result, error = await self.session(**args)

        if error:
            raise ComponentError(
                f"Error calling Network Ninja API: {error}"
            )

        if not result:
            raise DataNotFound(
                "No data returned from Network Ninja API"
            )

        return result
