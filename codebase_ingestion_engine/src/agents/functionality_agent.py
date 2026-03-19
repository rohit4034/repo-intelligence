import json

from src.core.llm.llm_client import LLMClient
from src.core.llm.prompt_manager import (
    _SYSTEM_PROMPT_PHASE1,
    _USER_PROMPT_PHASE1_TEMPLATE
)


class FunctionalityAgent:

    def __init__(self):
        self.llm = LLMClient()


    def run(self, capability):

        capability_json = json.dumps(capability, indent=2)

        user_prompt = _USER_PROMPT_PHASE1_TEMPLATE.format(
            source_code=capability_json
        )

        result = self.llm.generate(
            _SYSTEM_PROMPT_PHASE1,
            user_prompt
        )

        return result