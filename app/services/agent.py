from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor
from langchain.prompts import MessagesPlaceholder
import matplotlib.pyplot as plt
import io, base64

from ..core.config import settings

AGENT_PREFIX = """
You are a finance analyst working with a pandas DataFrame `df` of SIE-like transactions.
Rules:
- Use matplotlib.pyplot (no df.plot()).
- Don't call plt.show().
- Use plt.figure(figsize=(10,6)), titles, xlabel, ylabel, grid(True), tight_layout().
- Rotate x ticks 45°.
"""

def build_agent(df, memory: ConversationBufferMemory, model_name: str):
    base = create_pandas_dataframe_agent(
        ChatOpenAI(model=model_name, temperature=0, api_key=settings.openai_api_key),
        df,
        verbose=True,
        agent_type="openai-tools",
        allow_dangerous_code=True,
        prefix=AGENT_PREFIX,
        agent_kwargs={"extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")]},
    )
    executor = AgentExecutor.from_agent_and_tools(
        agent=base.agent,
        tools=base.tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
    )
    return executor

def capture_plot_as_base64_if_any():
    if not plt.get_fignums():
        return None
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close("all")
    return b64