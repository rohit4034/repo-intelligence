_SYSTEM_PROMPT_PHASE1 = """
You are a senior software analyst specialising in functional decomposition
of software systems.

Your job is to read a structured representation of a system capability
(derived from automated AST analysis of the codebase) and produce a
precise structured JSON object called a functionality_description.

Output ONLY JSON.
"""


_USER_PROMPT_PHASE1_TEMPLATE = """
Analyse the following structured capability description produced by automated AST analysis.

STRUCTURED INPUT:
\"\"\"
{source_code}
\"\"\"

Produce the functionality_description JSON exactly according to the schema provided.
"""


def build_prompt(capability_json):

    return _USER_PROMPT_PHASE1_TEMPLATE.format(
        source_code=capability_json
    )