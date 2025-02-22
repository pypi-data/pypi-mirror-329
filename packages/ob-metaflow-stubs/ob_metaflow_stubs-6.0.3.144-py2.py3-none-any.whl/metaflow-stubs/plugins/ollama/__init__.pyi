######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.14.2.1+obcheckpoint(0.1.8);ob(v1)                                                    #
# Generated on 2025-02-21T20:43:13.393866                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.card_utilities.injector
    import metaflow.decorators

from ...metaflow_current import current as current
from ...mf_extensions.outerbounds.plugins.ollama import ollama as ollama
from ...mf_extensions.outerbounds.plugins.ollama.ollama import OllamaManager as OllamaManager
from ...mf_extensions.outerbounds.plugins.card_utilities.injector import CardDecoratorInjector as CardDecoratorInjector

class OllamaDecorator(metaflow.decorators.StepDecorator, metaflow.mf_extensions.outerbounds.plugins.card_utilities.injector.CardDecoratorInjector, metaclass=type):
    """
    This decorator is used to run Ollama APIs as Metaflow task sidecars.
    
    User code call
    -----------
    @ollama(
        models=['meta/llama3-8b-instruct', 'meta/llama3-70b-instruct'],
        backend='local'
    )
    
    Valid backend options
    ---------------------
    - 'local': Run as a separate process on the local task machine.
    - (TODO) 'managed': Outerbounds hosts and selects compute provider.
    - (TODO) 'remote': Spin up separate instance to serve Ollama models.
    
    Valid model options
    ----------------
        - 'llama3.2'
        - 'llama3.3'
        - any model here https://ollama.com/search
    
    Parameters
    ----------
    models: list[Ollama]
        List of Ollama containers running models in sidecars.
    backend: str
        Determines where and how to run the Ollama process.
    """
    def task_decorate(self, step_func, flow, graph, retry_count, max_user_code_retries, ubf_context):
        ...
    ...

