from typing import List, Dict, Any, Optional
from ..core.exceptions import DataAccessError
from pydantic import BaseModel
import requests


class DatasetMap(BaseModel):
    index: str
    path: str


class DataAccessClient:
    def __init__(
        self,
        token: str,
        cached: bool = True,
        enabled: bool = True,
        data_access: List[Dict[str, Any]] = None,
    ):
        self.token = token
        self.cached = cached
        self.enabled = enabled
        self.data_access = data_access or []
        self.real_data_paths_map = {}
        self.url = "http://asset.internal.sais.com.cn/api/v1?type=dataset&q="

    def get_dataset(self, dataset_names: Optional[List[str]] = None) -> List[Dict]:
        # batch send dataset key id to assets platform to get virtual paths
        dataset_names = self.data_access[0].get("dataset_names")
        try:
            response = requests.get(
                f"{self.url}{dataset_names}",
                headers={"Content-Type": "application/json", "auth_token": self.token},
                verify=False,
            )
            response.raise_for_status()

            result: DatasetMap = response.json()

            if not isinstance(result, list):
                raise DataAccessError("Invalid response format")
            return result

        except requests.exceptions.RequestException as e:
            raise DataAccessError(f"Data access failed: {str(e)}") from e


def initialize(**kwargs) -> DataAccessClient:
    global client
    client = DataAccessClient(**kwargs)
    return client
