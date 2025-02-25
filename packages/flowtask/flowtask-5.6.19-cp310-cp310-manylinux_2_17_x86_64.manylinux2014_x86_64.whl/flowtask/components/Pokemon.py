import asyncio
from collections.abc import Callable
import math
from uuid import uuid4
from urllib.parse import urlencode, urljoin
from requests.models import PreparedRequest
import numpy as np
import pandas as pd
from .flow import FlowComponent
from ..interfaces.http import HTTPService
from ..exceptions import (
    ComponentError,
    DataError,
    DataNotFound
)


class Pokemon(HTTPService, FlowComponent):
    """
    Pokémon Component

    **Overview**

    This component interacts with the Pokémon API to retrieve data about machines or their on-hand inventory.
    It supports two main operations determined by the `type` parameter:

    - **"machines"**: Retrieves a list of machines.
    - **"inventory"**: Retrieves on-hand inventory data for specified machines.
    - **sites**: Retrieves the Pokemon sites
    - ****: Retrieves the Pokemon 
    - **warehouses**: Retrieves the Pokemon warehouses


    The component handles authentication, constructs the necessary requests, processes the data,
    and returns a pandas DataFrame suitable for further analysis in your data pipeline.

    .. table:: Properties
       :widths: auto

    +----------------------------+----------+----------------------------------------------------------------------------------------------+
    |   Name                     | Required | Summary                                                                                      |
    +----------------------------+----------+----------------------------------------------------------------------------------------------+
    |   credentials              | Yes      | Dictionary containing API credentials: `"BASE_URL"`, `"CLIENT_ID"`, and `"CLIENT_SECRET"`.   |
    |                            |          | Credentials can be retrieved from environment variables.                                     |
    +----------------------------+----------+----------------------------------------------------------------------------------------------+
    |   type                     | Yes      | Type of operation to perform. Accepts `"machines"` to retrieve machine data or `"inventory"` |
    |                            |          | to retrieve machine inventory data.                                                          |
    +----------------------------+----------+----------------------------------------------------------------------------------------------+
    |   ids                      | No       | List of machine IDs to retrieve inventory for when `type` is `"inventory"`.                  |
    |                            |          | Overrides IDs from the previous step if provided.                                            |
    +----------------------------+----------+----------------------------------------------------------------------------------------------+
    |   data                     | No       | Data from the previous step, typically a pandas DataFrame containing machine                 |
    |                            |          | IDs in a column named `"machine_id"`. Used when `type` is `"inventory"`.                     |
    +----------------------------+----------+----------------------------------------------------------------------------------------------+

    **Returns**

    This component returns a pandas DataFrame containing the retrieved data from the Pokémon API.
    The structure of the DataFrame depends on the operation type:

    - **For `type = "machines"`**: The DataFrame contains information about machines, with columns corresponding
        to the machine attributes provided by the API.
    - **For `type = "inventory"`**: The DataFrame contains on-hand inventory details for each machine,
        including `machineId` and detailed slot information.
    """  # noqa
    accept: str = "application/json"
    download = None
    _credentials: dict = {
        "BASE_URL": str,
        "CLIENT_ID": str,
        "CLIENT_SECRET": str,
    }
    ids: list = []
    errors_df: pd.DataFrame = None

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.type: str = kwargs.get('type')
        self.machine_inventory: bool = kwargs.get('machine_inventory', False)
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
            # Validate that machine_id column exists in the DataFrame
            if "machine_id" not in self.data.columns:
                raise ComponentError(
                    f'{__name__}: Input DataFrame must contain a "machine_id" column'
                )

        self.processing_credentials()

        # Adding client_id and secret:
        self.headers["client_id"] = self.credentials["CLIENT_ID"]
        self.headers["client_secret"] = self.credentials["CLIENT_SECRET"]

        return True

    async def run(self):
        type_call = getattr(self, f"{self.type}", None)

        if not type_call:
            raise ComponentError(
                "incorrect or not provided type"
            )

        if not callable(type_call):
            raise ComponentError(
                f"Function {self.type} doesn't exist."
            )

        try:
            result = await type_call()
        except (ComponentError, DataError, DataNotFound) as e:
            self._logger.error(f"Error: {str(e)}")
            raise

        if not isinstance(result, pd.DataFrame):
            self._result = result
            return self._result

        self.add_metric("NUMROWS", len(result.index))
        self.add_metric("NUMCOLS", len(result.columns))

        self._result = result

        if self._debug is True:
            self._print_data("Result Data", self._result)

        return self._result

    async def close(self):
        return True

    def _print_data(self, title: str, data_df: pd.DataFrame):
        """
        Prints the data and its corresponding column types for a given DataFrame.

        Parameters:
        title (str): The title to print before the data.
        data_df (pd.DataFrame): The DataFrame to print and inspect.
        """
        print(f"::: Printing {title} === ")
        print("Data: ", data_df)
        for column, t in data_df.dtypes.items():
            print(f"{column} -> {t} -> {data_df[column].iloc[0]}")

    def _create_url_arguments(self, method: str, path: str):
        """
        Creates the URL arguments for the given method and path.

        Parameters:
        method (str): The HTTP method for the request.
        path (str): The path for the request.

        Returns:
        dict: The URL arguments for the request.
        """
        self.headers["request-id"] = str(uuid4())
        url_args = {
            "method": method,
            "url": path,
            "use_proxy": False
        }
        return url_args

    async def _get_pokemon_results(self, args, payload):
        results, error = await self.session(**args, data=payload, use_json=True)

        if error:
            raise ComponentError(
                f"{__name__}: Error in request: {error}"
            )

        if not results:
            raise ComponentError(
                f"{__name__}: Empty response from API"
            )

        if "machines" in results:
            machines_data = []
            datetime_utc = results.get("dateTimeUTC")
            
            for machine in results["machines"]:
                machine_id = machine["machine"]
                slots = machine["slots"]
                
                if len(slots) == 1 and "errorCode" in slots[0]:
                    machines_data.append({
                        "machine": machine_id,
                        "slot": None,
                        "price": None,
                        "maxPar": None,
                        "count": None,
                        "isActive": None,
                        "productName": None,
                        "productBrand": None,
                        "productUpc": None,
                        "productLogisticsID": None,
                        "errorCode": slots[0].get("errorCode"),
                        "errorMessage": slots[0].get("errorMessage"),
                        "dateTimeUTC": datetime_utc
                    })
                    continue
                    
                for slot in slots:
                    machines_data.append({
                        "machine": machine_id,
                        "slot": slot.get("slot"),
                        "price": slot.get("price"),
                        "maxPar": slot.get("maxPar"),
                        "count": slot.get("count"),
                        "isActive": slot.get("isActive"),
                        "productName": slot.get("productName"),
                        "productBrand": slot.get("productBrand"),
                        "productUpc": slot.get("productUpc"),
                        "productLogisticsID": slot.get("productLogisticsID"),
                        "errorCode": None,
                        "errorMessage": None,
                        "dateTimeUTC": datetime_utc
                    })
            
            df = pd.DataFrame(machines_data)
            
            column_order = [
                "machine", "slot", "productName", "productBrand", "productUpc",
                "productLogisticsID", "price", "maxPar", "count", "isActive",
                "dateTimeUTC", "errorCode", "errorMessage"
            ]
            df = df[column_order]
            
            return df
        else:
            raise ComponentError(
                f"{__name__}: Unexpected response format: {results}"
            )

    def get_pokemon_url(self, resource, parameters: dict = None):
        url = urljoin(self.credentials["BASE_URL"], resource)
        if parameters:
            url += "?" + urlencode(parameters)
        return url

    def get_machines_inventory_payload(self, machines: list):
        """Create payload following API specification"""
        return {
            "requestFilter": {
                "machines": machines
            }
        }

    @staticmethod
    def split_chunk_ids(items: pd.Series, chunk_size: str):
        """
        Splits a Series of IDs into chunks of a specified size.

        Parameters:
        items (pd.Series): A pandas Series containing the IDs to be split.
        chunk_size (int): The maximum number of IDs per chunk.

        Returns:
        list: A list of NumPy arrays, each containing a chunk of IDs.
            If the Series is empty or all IDs are NaN, returns an empty list or a list containing an empty array.
        """
        data = items.dropna().unique().astype(str)

        if data.size > 0:
            split_n = math.ceil(data.size / chunk_size)

            # Split into chunks of n items
            return np.array_split(data, split_n)  # Convert to NumPy array and split

        return [data]

    async def inventory(self):
        args = self._create_url_arguments(
            method="post",
            path=self.get_pokemon_url("machines/on-hand-inventory"),
        )
        
        # List of Machine IDs - Check both input sources
        if hasattr(self, 'data') and isinstance(self.data, pd.DataFrame) and not self.data.empty:
            if "machine_id" not in self.data.columns:
                raise ComponentError(
                    f'{__name__}: Input DataFrame must contain a "machine_id" column'
                )
            self._logger.info(
                f'{__name__}: Using machine_ids from previous step in column "machine_id"'
            )
            self.data_ids = self.data["machine_id"]
        elif self.ids and len(self.ids) > 0:
            self._logger.info(f"{__name__}: Using machine_ids provided in Task arguments")
            self.data_ids = pd.Series(self.ids)
        else:
            raise ComponentError(
                f'{__name__}: No machine_ids provided. Either pass them through previous step with "machine_id" column or specify in task arguments'
            )

        # Validate we have valid IDs
        if self.data_ids.empty:
            raise ComponentError(f"{__name__}: No valid machine_ids found to process")

        total_ids = len(self.data_ids)
        self._logger.info(f"Processing {total_ids} machine_ids")

        # Split into chunks of 4 (API limit)
        ids_chunks = self.split_chunk_ids(
            items=self.data_ids,
            chunk_size=4,
        )
        
        total_chunks = len(ids_chunks)
        self._logger.info(f"Split into {total_chunks} chunks of max 4 machines each")

        # Process chunks with error handling and progress
        df_items = pd.DataFrame()
        errors = []
        
        for i, ids_chunk in enumerate(ids_chunks, 1):
            try:
                self._logger.info(f"Requesting inventory for machines: {ids_chunk.tolist()}")
                payload = self.get_machines_inventory_payload(ids_chunk.tolist())
                items = await self._get_pokemon_results(args, payload)
                df_items = pd.concat([df_items, items], ignore_index=True)
                
                # Optional: Add small delay to avoid overwhelming the API
                if i < total_chunks:  # Don't delay after last chunk
                    await asyncio.sleep(0.5)  # 500ms delay between chunks
                    
            except Exception as e:
                error_msg = f"Error processing chunk {i}/{total_chunks} - IDs: {ids_chunk.tolist()} - Error: {str(e)}"
                self._logger.error(error_msg)
                errors.append({
                    'chunk': i,
                    'ids': ids_chunk.tolist(),
                    'error': str(e)
                })
                continue  # Continue with next chunk even if this one fails

        # Log summary
        processed_machines = len(df_items.index)
        self._logger.info(f"Finished processing {processed_machines}/{total_ids} machines")
        
        if errors:
            self._logger.warning(f"Found {len(errors)} errors during processing")
            errors_df = pd.DataFrame(errors)
            self.errors_df = errors_df  # Save errors for later inspection
            
        if df_items.empty:
            raise ComponentError(f"{__name__}: No data could be retrieved from any chunk")

        return df_items

    async def _get_pokemon_resource(self, resource: str = 'sites', response_key: str = None):
        """Get a Pokemon Resource with optional Pagination (as sites, or )

        Args:
            resource (str, optional): The resource to get (default'sites').
            response_key (str, optional): The key to look for in the API response. If None, uses the resource name.

        Return:
            pd.DataFrame: The DataFrame containing the requested resource.

        """
        result = []
        offset = None
        off_args = None
        
        # If no response_key provided, use the resource name
        response_key = response_key or resource
        
        while True:
            if offset:
                off_args = {"offset": offset}
            args = self._create_url_arguments(
                method="get",
                path=self.get_pokemon_url(resource, off_args),
            )
            results, error = await self.session(**args)
            if error:
                raise DataError(
                    f"Error getting Pokemon {resource.capitalize()} {error}"
                )
            
            if not results:
                self._logger.warning(f"Empty response received for {resource}")
                break
            
            if r := results.get(response_key, []):

                result.extend(r)
            else:
                break
            
            offset = results.get('offset', None)
            if offset is None:
                break
            
        if not result:
            raise DataNotFound(f"No Pokemon {resource.capitalize()} found")
        return await self.create_dataframe(result)

    async def sites(self):
        return await self._get_pokemon_resource('sites')

    async def locations(self):
        return await self._get_pokemon_resource('locations')
    
    async def kiosks_history(self):
        return await self._get_pokemon_resource('machines/installs', 'machineInstalls')

    async def products(self):
        return await self._get_pokemon_resource('products')

    async def warehouses(self):
        args = self._create_url_arguments(
            method="get",
            path=self.get_pokemon_url("warehouses/merch")
        )
        results, error = await self.session(**args)

        if result := results.get("merchWarehouses", None):
            return await self.create_dataframe(result)
        else:
            raise ComponentError(
                f"{__name__}: Error in Machines request: {error} {results}"
            )

    async def machines(self):
        args = self._create_url_arguments(
            method="get",
            path=self.get_pokemon_url("machines")
        )
        results, error = await self.session(**args)

        if result := results.get("machines", None):
            return await self.create_dataframe(result)
        else:
            raise ComponentError(
                f"{__name__}: Error in Machines request: {error} {results}"
            )

    async def health(self):
        args = self._create_url_arguments(
            method="get",
            path=self.get_pokemon_url("health-check")
        )
        result, error = await self.session(**args)

        if message := result.get("message", None):
            if message == "The ar-vending-prc-api is up and running":
                return result
            else:
                return result
        else:
            raise ComponentError(
                f"{__name__}: Error in Health request: {error}"
            )