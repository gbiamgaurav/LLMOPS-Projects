
# Chat Models
from langchain_groq import ChatGroq
#from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch

# Agents
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage
from app.config.settings import Settings


def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):

    llm = ChatGroq(model=llm_id)
    tools = [TavilySearch(max_results=3)] if allow_search else []
    agent = create_react_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
    )

    state = {"messages": query}

    response = agent.invoke(state)

    messages = response.get("messages")

    ai_messages = [message.content for message in messages if isinstance(message, AIMessage)]

    return ai_messages[-1]



