from fastapi import FastAPI, Depends, Query
from llama_index.core.agent import ReActAgent
from ai_assistant.agent import TravelAgent
from ai_assistant.models import AgentAPIResponse
from ai_assistant.prompts import agent_prompt_tpl
from ai_assistant.tools import (
    reserve_bus,
    reserve_hotel,
    reserve_restaurant,
    reserve_flight,
    delete_all_reservations

)

def get_agent() -> ReActAgent:
    return TravelAgent(agent_prompt_tpl).get_agent()


app = FastAPI(title="AI Agent")


@app.get("/recommendations/cities")
def recommend_cities(
    notes: list[str] = Query(...), agent: ReActAgent = Depends(get_agent)
):
    prompt = f"recommend cities in bolivia with the following notes: {notes if notes else 'No specific notes'}"
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))
@app.get("/recommendations/places")
def recommend_places(city: str, notes: list[str] = Query(None), agent: ReActAgent = Depends(get_agent)):
    
    prompt = f"recommend places to visit in {city} with the following notes: {notes if notes else 'No specific notes'}"
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))
@app.get("/recommendations/activities")
def recommend_places(city: str, notes: list[str] = Query(None), agent: ReActAgent = Depends(get_agent)):
    
    prompt = f"recommend activities to do in {city} with the following notes: {notes if notes else 'No specific notes'}"
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))
@app.get("/recommendations/hotels")
def recommend_places(city: str, notes: list[str] = Query(None), agent: ReActAgent = Depends(get_agent)):
    
    prompt = f"recommend hotels to stay at in {city} with the following notes: {notes if notes else 'No specific notes'}"
    return AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))
@app.post("/reserve/bus")
def reserve_bus_ticket_api(origin: str, destination: str, date: str):
    
    reservation = reserve_bus(date, origin, destination)
    return {"status": "OK", "reservation": reservation.dict()}
@app.post("/reserve/hotel")
def reserve_hotel_api(checkin_date_str: str, checkout_date_str: str, hotel_name: str, city: str):
    reservation = reserve_hotel(checkin_date_str, checkout_date_str, hotel_name, city)
    return {"status": "OK", "reservation": reservation.dict()}
@app.post("/reserve/flight")
def reserve_flight_api(origin: str, destination: str, date: str):
    reservation = reserve_flight(date, origin, destination)
    return {"status": "OK", "reservation": reservation.dict()}
@app.post("/reserve/restaurant")
def reserve_restaurant_api(reservation_time_str: str, restaurant: str, city: str, dish: str = None):
    reservation = reserve_restaurant(reservation_time_str, restaurant, city, dish)
    return {"status": "OK", "reservation": reservation.dict()}

@app.get("/trip/report")
def trip_summary(agent: ReActAgent = Depends(get_agent)):

    prompt = """
        Generate a trip summary using the tool `trip_summary_tool`.
        Once the summary is generated, analyze it and provide a detailed report.

        The detailed report should contain:
        1. Key highlights of the trip.
        2. Identified issues or recommendations.
        3. Additional insights based on the trip summary.

        Begin by creating the trip summary with `trip_summary_tool`, then proceed with the analysis and report.

        Ensure both the trip summary and the detailed report are in **Spanish** and are included in your **final Answer**.
        Do not include any internal thoughts or reasoning—only return the final answer containing the summary and report.
    """

    response = agent.chat(prompt)
    
    return AgentAPIResponse(
        status="OK",
        agent_response=str(response)
    )

@app.delete("/trip/delete-all")
def delete_all_trip_reservations():
    delete_all_reservations()
    return {"status": "success", "message": "All trip reservations have been deleted."}