from typing import Optional, Dict
import pandas as pd
from langchain.memory import ConversationBufferMemory

df: Optional[pd.DataFrame] = None
SESSIONS: Dict[str, ConversationBufferMemory] = {}