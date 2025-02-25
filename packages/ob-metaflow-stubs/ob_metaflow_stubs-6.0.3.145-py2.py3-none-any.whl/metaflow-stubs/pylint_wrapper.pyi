######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.14.3.1+obcheckpoint(0.1.8);ob(v1)                                                    #
# Generated on 2025-02-24T18:52:39.106598                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from .exception import MetaflowException as MetaflowException

class PyLintWarn(metaflow.exception.MetaflowException, metaclass=type):
    ...

class PyLint(object, metaclass=type):
    def __init__(self, fname):
        ...
    def has_pylint(self):
        ...
    def run(self, logger = None, warnings = False, pylint_config = []):
        ...
    ...

