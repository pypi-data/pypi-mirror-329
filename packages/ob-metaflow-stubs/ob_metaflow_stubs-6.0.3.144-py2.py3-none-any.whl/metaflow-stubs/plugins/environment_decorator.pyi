######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.14.2.1+obcheckpoint(0.1.8);ob(v1)                                                    #
# Generated on 2025-02-21T20:43:13.432403                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators


class EnvironmentDecorator(metaflow.decorators.StepDecorator, metaclass=type):
    """
    Specifies environment variables to be set prior to the execution of a step.
    
    Parameters
    ----------
    vars : Dict[str, str], default {}
        Dictionary of environment variables to set.
    """
    def runtime_step_cli(self, cli_args, retry_count, max_user_code_retries, ubf_context):
        ...
    ...

