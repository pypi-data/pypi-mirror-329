"""A Databricks implementation of the PyAirbyte cache.

## Usage Example

```python
from airbyte as ab
from airbyte.caches import DatabricksCache

cache = DatabricksCache(
    access_token = ab.get_secret("databricks_access_token"),
    server_hostname = ab.get_secret("databricks_server_hostname"),
    http_path= ab.get_secret("databricks_http_path"),
    catalog = ab.get_secret("databricks_catalog"),
    schema_name = ab.get_secret("databricks_target_schema"),
    staging_volume_w_location = ab.get_secret("databricks_staging_volume_w_location")
)
```

staging_volume_w_location =>    Is a temporarly location that is needed to upload the data before inserting into the table. 
                                It must be a Databricks Volume e.g. "/Volumes/<catalog_name>/<schema_name>/<volume_name>"
                                Read more about volumes here: https://docs.databricks.com/en/volumes/index.html
"""

from __future__ import annotations

from pydantic import PrivateAttr

from airbyte_databricks_cache._processors.sql.databricks import DatabricksConfig, DatabricksSqlProcessor
from airbyte.caches.base import CacheBase

class DatabricksCache(DatabricksConfig, CacheBase):
    _sql_processor_class = PrivateAttr(default=DatabricksSqlProcessor)
    

__all__ = [
    "DatabricksCache",
    "DatabricksConfig",
]    