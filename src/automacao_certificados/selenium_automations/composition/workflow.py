
from automacao_certificados.selenium_automations.application.workflow import WorkflowSelector
from automacao_certificados.selenium_automations.composition.adapters import AdapterFactory

class WorkflowFactory:
    def __init__(self, adapter_factory: AdapterFactory):
        if not isinstance(adapter_factory, AdapterFactory):
            raise ValueError("adapter_factory must be of type AdapterFactory")

        self.adapter_factory = adapter_factory

    def create_workflow_selector(self) -> WorkflowSelector:
        return WorkflowSelector(
            municipio_api_requester=self.adapter_factory.create_receita_api_municipio_getter()
        )
    