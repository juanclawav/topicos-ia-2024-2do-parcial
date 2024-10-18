from random import randint
from datetime import date, datetime, time
from llama_index.core.tools import QueryEngineTool, FunctionTool, ToolMetadata
from ai_assistant.rags import TravelGuideRAG
from ai_assistant.prompts import travel_guide_qa_tpl, travel_guide_description
from ai_assistant.config import get_agent_settings
from ai_assistant.models import (
    TripReservation,
    TripType,
    HotelReservation,
    RestaurantReservation,
)
from ai_assistant.utils import save_reservation

SETTINGS = get_agent_settings()

travel_guide_tool = QueryEngineTool(
    query_engine=TravelGuideRAG(
        store_path=SETTINGS.travel_guide_store_path,
        data_dir=SETTINGS.travel_guide_data_path,
        qa_prompt_tpl=travel_guide_qa_tpl,
    ).get_query_engine(),
    metadata=ToolMetadata(
        name="travel_guide", description=travel_guide_description, return_direct=False
    ),
)


# Tool functions
def reserve_flight(date_str: str, departure: str, destination: str) -> TripReservation:
    """
    ===> COMPLETE DESCRIPTION HERE <===
    """
    print(
        f"Making flight reservation from {departure} to {destination} on date: {date}"
    )
    reservation = TripReservation(
        trip_type=TripType.flight,
        departure=departure,
        destination=destination,
        date=date.fromisoformat(date_str),
        cost=randint(200, 700),
    )

    save_reservation(reservation)
    return reservation

def reserve_bus(date_str: str, departure: str, destination: str) -> TripReservation:
    """
    Reserva un boleto de bus.
    
    Parámetros:
    - date_str: Fecha del viaje (string, formato ISO).
    - departure: Ciudad de origen.
    - destination: Ciudad de destino.
    
    Retorno:
    - TripReservation: Objeto con detalles de la reserva.
    """
    print(f"Making bus reservation from {departure} to {destination} on date: {date_str}")
    reservation = TripReservation(
        trip_type=TripType.bus,
        departure=departure,
        destination=destination,
        date=date.fromisoformat(date_str),
        cost=randint(10, 50),
    )
    
    save_reservation(reservation)
    return reservation

def reserve_hotel(checkin_date_str: str, checkout_date_str: str, hotel_name: str, city: str) -> HotelReservation:
    """
    Reserva una habitación de hotel.
    
    Parámetros:
    - checkin_date_str: Fecha de check-in (string, formato ISO).
    - checkout_date_str: Fecha de check-out (string, formato ISO).
    - hotel_name: Nombre del hotel.
    - city: Ciudad donde se encuentra el hotel.
    
    Retorno:
    - HotelReservation: Objeto con detalles de la reserva.
    """
    print(f"Making hotel reservation at {hotel_name} in {city} from {checkin_date_str} to {checkout_date_str}")
    reservation = HotelReservation(
        checkin_date=date.fromisoformat(checkin_date_str),
        checkout_date=date.fromisoformat(checkout_date_str),
        hotel_name=hotel_name,
        city=city,
        cost=randint(100, 1000),
    )
    
    save_reservation(reservation)
    return reservation


def reserve_restaurant(reservation_time_str: str, restaurant: str, city: str, dish: str = None) -> RestaurantReservation:
    """
    Reserva una mesa de un restaurante.
    
    Parámetros:
    - reservation_time_str: Hora de la reserva (string, formato ISO).
    - restaurant: Nombre del restaurante.
    - city: Ciudad donde se encuentra el restaurante.
    - dish: Nombre de la comida (opcional).
    
    Retorno:
    - RestaurantReservation: Objeto con detalles de la reserva.
    """
    print(f"Making restaurant reservation at {restaurant} in {city} at {reservation_time_str}")
    reservation = RestaurantReservation(
        reservation_time=datetime.fromisoformat(reservation_time_str),
        restaurant=restaurant,
        city=city,
        dish=dish,
        cost=randint(10, 50),
    )      
    
    save_reservation(reservation)   
    return reservation




flight_tool = FunctionTool.from_defaults(fn=reserve_flight, return_direct=False)
bus_tool = FunctionTool.from_defaults(fn=reserve_bus, return_direct=False)
hotel_tool = FunctionTool.from_defaults(fn=reserve_hotel, return_direct=False)
restaurant_tool = FunctionTool.from_defaults(fn=reserve_restaurant, return_direct=False)
