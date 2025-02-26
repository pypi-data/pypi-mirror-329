######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.0.1+obcheckpoint(0.1.8);ob(v1)                                                    #
# Generated on 2025-02-25T21:49:22.565629                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.event_logger


class DebugEventLogger(metaflow.event_logger.NullEventLogger, metaclass=type):
    @classmethod
    def get_worker(cls):
        ...
    ...

class DebugEventLoggerSidecar(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    ...

