import sys
from airbyte_databricks_cache._processors.sql import databricks as _A
from airbyte_databricks_cache.caches import databricks as _B

#
## HACK
# create modules 
# - airbyte._processors.sql.databricks 
# - airbyte.caches.databricks
# and inject the specific classes/functions it in
#

sys.modules['airbyte._processors.sql.databricks'] = _A
sys.modules['airbyte.caches.databricks'] = _B

## end of HACK