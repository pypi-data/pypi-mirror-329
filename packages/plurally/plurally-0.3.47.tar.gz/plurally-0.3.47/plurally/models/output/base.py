import enum

from rq import get_current_job

from plurally.models.node import Node


class OutputType(str, enum.Enum):
    TEXT = "text"
    HTML = "html"
    CRM_ACTIONS = "crm_actions"
    TABLE = "table"


class BaseOutput(Node):
    def _get_output_content(self, node_input):
        raise NotImplementedError

    def _get_output_type(self) -> OutputType:
        raise NotImplementedError

    def build_output(self, node_input):
        return {"type": self._get_output_type().value, "content": self._get_output_content(node_input)}

    def forward(self, node_input):
        current_job = get_current_job()
        if current_job:
            output = current_job.meta.get("output", {})
            output[self.name] = self.build_output(node_input)
            current_job.meta["output"] = output
            current_job.save_meta()
