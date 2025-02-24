"""Base module for all caches."""

from __future__ import annotations

############## HACKS ################
#
## HACK
# put kwargs.next_page_token.next_page_token into self.config.next_page_token. read more in comments below/
#

from airbyte_cdk.sources.declarative.requesters.request_options.interpolated_nested_request_input_provider import InterpolatedNestedRequestInputProvider
def hacked_eval_request_inputs(self, stream_slice, next_page_token) :
    kwargs = {
            # "stream_state": stream_state, # stream_state removed from newer version of CDK
            "stream_slice": stream_slice,
            "next_page_token": next_page_token,
        }
    ##  
    # HACK is this: put kwargs.next_page_token.next_page_token into self.config.next_page_token, so it can be referenced as config.next_page_token
    # this solves: https://github.com/airbytehq/airbyte/issues/40697 for now
    ##
    self.config['next_page_token'] = kwargs.get('next_page_token').get('next_page_token') if kwargs.get('next_page_token') else None
    return self._interpolator.eval(self.config, **kwargs)

InterpolatedNestedRequestInputProvider.eval_request_inputs = hacked_eval_request_inputs

## end of HACK



from airbyte_databricks_cache.caches import databricks
from airbyte_databricks_cache.caches.databricks import DatabricksCache



# We export these classes for easy access: `airbyte_.caches...`
__all__ = [
    # Factories
    #
    # Classes
    "DatabricksCache",
    # Submodules,
    "databricks",
]
