from random import randint
from datetime import date, datetime, time
from llama_index.core.tools import QueryEngineTool, FunctionTool, ToolMetadata
from ai_assistant.rags import TravelGuideRAG
from ai_assistant.prompts import travel_guide_qa_tpl, travel_guide_description
from ai_assistant.config import get_agent_settings
import json
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
    )
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

def generate_trip_summary() -> str:
    """
    Generates a detailed summary of the trip based on the reservations logged in trip.json.
    It organizes the activities by type (flight, hotel, bus, restaurant), date, and location, 
    and provides a total cost summary.
    
    Returns:
    - A string summarizing the entire trip including all reserved activities and their costs.
    """
    try:
        # Leer el archivo trip.json que contiene todas las reservas
        with open(SETTINGS.log_file, 'r') as file:
            reservations = json.load(file)
        
        if not reservations:
            return "No reservations found for the trip."
        
        # Inicializar variables
        summary = "📝 **Trip Summary**\n\n"
        total_cost = 0
        activities_by_city = {}

        # Organizar las actividades por ciudad y fecha
        for reservation in reservations:
            city = reservation.get('city', reservation.get('destination'))  # Se usa 'city' o 'destination'
            date = reservation.get('date') or reservation.get('checkin_date') or reservation.get('reservation_time')
            cost = reservation.get('cost', 0)
            total_cost += cost

            if city not in activities_by_city:
                activities_by_city[city] = []

            activities_by_city[city].append({
                'type': reservation.get('reservation_type'),
                'date': date,
                'details': reservation
            })
        
        # Crear el reporte detallado por ciudad y por tipo de actividad
        for city, activities in activities_by_city.items():
            summary += f"**City: {city}**\n"
            for activity in sorted(activities, key=lambda x: x['date']):
                activity_type = activity['type']
                activity_date = activity['date']
                details = activity['details']
                
                summary += f"- {activity_type} on {activity_date}:\n"
                if activity_type == "TripReservation":
                    trip_type = details.get('trip_type', 'Unknown')
                    summary += f"  🚗 {trip_type} from {details['departure']} to {details['destination']}, Cost: ${details['cost']}\n"
                elif activity_type == "HotelReservation":
                    summary += f"  🏨 Hotel {details['hotel_name']} from {details['checkin_date']} to {details['checkout_date']}, Cost: ${details['cost']}\n"
                elif activity_type == "RestaurantReservation":
                    summary += f"  🍽️ Restaurant {details['restaurant']} at {details['reservation_time']}, Cost: ${details['cost']}\n"

            summary += "\n"

        # Añadir el costo total al final del reporte
        summary += f"**Total Trip Cost: ${total_cost}**\n"
        return summary
    
    except FileNotFoundError:
        return "The trip log file (trip.json) was not found."
    except json.JSONDecodeError:
        return "Error reading the trip log file. It may be corrupted."

flight_tool = FunctionTool.from_defaults(fn=reserve_flight, return_direct=False)
bus_tool = FunctionTool.from_defaults(fn=reserve_bus, return_direct=False)
hotel_tool = FunctionTool.from_defaults(fn=reserve_hotel, return_direct=False)
restaurant_tool = FunctionTool.from_defaults(fn=reserve_restaurant, return_direct=False)
trip_summary_tool = FunctionTool.from_defaults(fn=generate_trip_summary, return_direct=False)
