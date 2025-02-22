######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.14.2.1+obcheckpoint(0.1.8);ob(v1)                                                    #
# Generated on 2025-02-21T20:43:13.431539                                                            #
######################################################################################################

from __future__ import annotations

import abc
import typing
if typing.TYPE_CHECKING:
    import abc

from . import secrets_decorator as secrets_decorator
from . import inline_secrets_provider as inline_secrets_provider

class SecretsProvider(abc.ABC, metaclass=abc.ABCMeta):
    def get_secret_as_dict(self, secret_id, options = {}, role = None) -> typing.Dict[str, str]:
        """
        Retrieve the secret from secrets backend, and return a dictionary of
        environment variables.
        """
        ...
    ...

