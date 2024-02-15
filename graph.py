import json

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

from agents import AgentState, create_supervisor, create_search_agent, create_insights_researcher_agent, get_members

def build_graph():
  supervisor_chain = create_supervisor()
  search_node = create_search_agent()
  insights_research_node = create_insights_researcher_agent()

  graph_builder = StateGraph(AgentState)
  graph_builder.add_node("Supervisor", supervisor_chain)
  graph_builder.add_node("Web_Searcher", search_node)
  graph_builder.add_node("Insight_Researcher", insights_research_node)
  
  members =  get_members()
  for member in members:
    graph_builder.add_edge(member, "Supervisor")

  conditional_map = {k: k for k in members}
  conditional_map["FINISH"] = END
  graph_builder.add_conditional_edges("Supervisor", lambda x: x["next"], conditional_map)
  graph_builder.set_entry_point("Supervisor")

  graph = graph_builder.compile()

  return graph

def run_graph(input_message):
  graph = build_graph()
  response = graph.invoke({
      "messages": [HumanMessage(content=input_message)]
  })

  return json.dumps(response['messages'][1].content, indent=2)