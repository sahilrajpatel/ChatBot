from typing import TypedDict, Annotated
import operator

from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from src import config
from src.tools import TOOLS

llm = ChatOpenAI(
    model=config.CHAT_MODEL,
    temperature=0,
    api_key=config.OPENAI_API_KEY,
).bind_tools(TOOLS)

SYSTEM_PROMPT = SystemMessage(
    content=(
        "You are a helpful chatbot that has access to the internet. "
        "Use the web_search tool whenever the user asks about something "
        "real-time - like news, weather, prices, scores, current events, "
        "or anything you're not 100% sure is still true. "
        "Use the read_website tool when the user gives you a specific link. "
        "If a normal question doesn't need live data, just answer directly."
    )
)


# state = the list of messages in the conversation so far
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]


def call_model(state: ChatState) -> ChatState:
    messages = [SYSTEM_PROMPT] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}


def should_continue(state: ChatState) -> str:
    last_message = state["messages"][-1]
    # if the model asked to call a tool, go run the tool, else we're done
    if last_message.tool_calls:
        return "tools"
    return END


def build_graph():
    graph = StateGraph(ChatState)

    graph.add_node("agent", call_model)
    graph.add_node("tools", ToolNode(TOOLS))

    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")  # after tool runs, go back to the model

    return graph.compile()
