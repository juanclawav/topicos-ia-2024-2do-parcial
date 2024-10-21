from llama_index.core import PromptTemplate
from llama_index.core.agent import ReActAgent
from ai_assistant.tools import (
    travel_guide_tool,
    flight_tool,
    hotel_tool,    # <-- Añadir
    bus_tool,      # <-- Añadir
    restaurant_tool, # <-- Añadir
    trip_summary_tool,
    trip_planner_tool
)


class TravelAgent:
    def __init__(self, system_prompt: PromptTemplate | None = None):
        self.agent = ReActAgent.from_tools(
            [
                travel_guide_tool,
                flight_tool,
                hotel_tool,    # <-- Añadir
                bus_tool,      # <-- Añadir
                restaurant_tool,
                trip_summary_tool,
                trip_planner_tool
            ],
            verbose=True,
        )

        if system_prompt is not None:
            self.agent.update_prompts({"agent_worker:system_prompt": system_prompt})

    def get_agent(self) -> ReActAgent:
        return self.agent
