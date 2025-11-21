from abc import ABC, abstractmethod
from automacao_certificados.selenium_automations.application.workflow.workflow import Workflow

class WorkflowFactory(ABC):
    @abstractmethod
    def get_workflow(self) -> Workflow:
        pass