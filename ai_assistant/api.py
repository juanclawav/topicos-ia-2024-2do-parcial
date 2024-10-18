from fastapi import FastAPI, Depends, Query
from llama_index.core.agent import ReActAgent
from ai_assistant.agent import TravelAgent
from ai_assistant.models import AgentAPIResponse
from ai_assistant.tools import (
    reserve_bus,
    generate_trip_summary
)


def get_agent() -> ReActAgent:
    return TravelAgent().get_agent()


app = FastAPI(title="AI Agent")


@app.get("/recommendations/cities")
def recommend_cities(
    notes: list[str] = Query(None), agent: ReActAgent = Depends(get_agent)
):
    prompt = f"recommend cities in bolivia with the following notes: {notes if notes else 'No specific notes'}"
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))
@app.get("/recommendations/places")
def recommend_places(city: str, notes: list[str] = Query(None), agent: ReActAgent = Depends(get_agent)):
    
    prompt = f"recommend places to visit in {city} with the following notes: {notes if notes else 'No specific notes'}"
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))
@app.post("/reserve/bus")
def reserve_bus_ticket(origin: str, destination: str, date: str):
    reservation = reserve_bus(date, origin, destination)
    return {"status": "OK", "reservation": reservation.dict()}
@app.get("/trip/report")
def trip_report(agent: ReActAgent = Depends(get_agent)):
    report = generate_trip_summary()
    return AgentAPIResponse(status="OK", agent_response=report)
