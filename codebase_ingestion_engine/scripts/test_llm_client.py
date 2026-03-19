import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from src.core.llm.llm_client import LLMClient


SYSTEM_PROMPT = "You are a helpful assistant."
USER_PROMPT = "Explain what a Python function does in one sentence."


def main():

    llm = LLMClient()

    result = llm.generate(
        SYSTEM_PROMPT,
        USER_PROMPT
    )

    print("\nLLM RESPONSE:\n")
    print(result)


if __name__ == "__main__":
    main()