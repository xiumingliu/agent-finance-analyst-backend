## app/prompts/loader.py
from importlib import resources

def load_text(package: str, name: str) -> str:
    """
    Load a text file shipped in the package.
    Example: load_text("app.prompts", "finance_agent_prefix.md")
    """
    with resources.files(package).joinpath(name).open("r", encoding="utf-8") as f:
        return f.read()

def compose_finance_agent_prefix() -> str:
    core = load_text("app.prompts", "finance_agent_prefix.md")
    fpna = load_text("app.prompts", "fpna_cashflow_knowledge.md")
    # Keep the core first; append business knowledge.
    return f"{core}\n\n{fpna}\n"