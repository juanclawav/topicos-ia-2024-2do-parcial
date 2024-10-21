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
    Reserves a plane ticket
    
    Parameters:
    - date_str: Date of the trip (string, ISO format).
    - departure: City of departure.
    - destination: City of destination.
    
    Returns:
    - TripReservation: Reerve details object.
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
    Reserves a bus.
    
    Parameters:
    - date_str: Date of trip (string, ISO format).
    - departure: Ciuty of departure.
    - destination: City of destination.
    
    Returns:
    - TripReservation: Reservation details object.
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
    Book a hotel room.

    Parameters:

    -checkin_date_str: Check-in date (string, ISO format).
    -checkout_date_str: Check-out date (string, ISO format).
    -hotel_name: Name of the hotel.
    -city: City where the hotel is located.
    Return:

    HotelReservation: Object containing reservation details.
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
    Book a restaurant table.

    Parameters:

    reservation_time_str: Reservation time (string, ISO format).
    restaurant: Name of the restaurant.
    city: City where the restaurant is located.
    dish: Name of the dish (optional).
    Return:

    RestaurantReservation: Object containing reservation details.
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
                    summary += f"  {trip_type} from {details['departure']} to {details['destination']}, Cost: ${details['cost']}\n"
                elif activity_type == "HotelReservation":
                    summary += f"   Hotel {details['hotel_name']} from {details['checkin_date']} to {details['checkout_date']}, Cost: ${details['cost']}\n"
                elif activity_type == "RestaurantReservation":
                    summary += f"   Restaurant {details['restaurant']} at {details['reservation_time']}, Cost: ${details['cost']}\n"

            summary += "\n"

        # Añadir el costo total al final del reporte
        summary += f"**Total Trip Cost: ${total_cost}**\n"
        return summary
    
    except FileNotFoundError:
        return "The trip log file (trip.json) was not found."
    except json.JSONDecodeError:
        return "Error reading the trip log file. It may be corrupted."
    


def generate_itinerary(budget: int, start_date_str: str, days: int) -> dict:

    """
    Genera un itinerario de viaje basado en un presupuesto y un rango de días.
    Utiliza las herramientas disponibles, incluyendo `TravelGuideRAG`, para reservar vuelos, buses, hoteles, restaurantes y actividades.
    
    Parámetros:
    - budget: Presupuesto máximo (en dólares).
    - start_date_str: Fecha de inicio del viaje (string, formato ISO YYYY-MM-DD).
    - days: Duración del viaje (número de días).
    
    Retorno:
    - itinerary: Diccionario con el itinerario detallado y el costo total.
    """
    from datetime import datetime, timedelta
    from random import randint
    from llama_index.core.agent import ReActAgent
    from ai_assistant.agent import TravelAgent
    from ai_assistant.prompts import agent_prompt_tpl
    from ai_assistant.tools import travel_guide_tool
    from ai_assistant.models import AgentAPIResponse
    from fastapi import FastAPI, Depends, Query

    
    
     

    start_date = datetime.fromisoformat(start_date_str)
    current_budget = budget
    itinerary = []
    
    # Consultar al travel guide para obtener ciudades y recomendaciones
    agent = ReActAgent.from_tools([travel_guide_tool], verbose=False)
    prompt = f"Recommend cities to visit in Bolivia, only city names no details, do not suggest La Paz, list them like this: Ciudad:(Name of city)  "
    travel_guide_response = AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))
   
    if isinstance(travel_guide_response, AgentAPIResponse):
            cities_response = travel_guide_response.agent_response
    # Parsear las ciudades del travel guide
    cities = extract_cities_from_response(cities_response)
    
    if not cities:
        return {"error": "No se pudieron obtener ciudades del Travel Guide."}

    # Iterar por cada día del itinerario
    for i in range(days):
        current_date = start_date + timedelta(days=i)
        city = cities[i % len(cities)]  # Alternar entre las ciudades obtenidas del travel guide

        # Obtener detalles de la ciudad usando el Travel Guide
        prompt = f"¿Qué lugares, hoteles y restaurantes recomiendas en {city}? Dame listas en este formato: Hotels: (list of one hotel each line starting in the next line)  Places to Visit: (list of one place each line starting in the next line)  Restaurants: (list of one restaurant each line starting in the next line)"
        city_details = AgentAPIResponse(status="OK", agent_response=str(agent.chat(prompt)))
        if isinstance(city_details, AgentAPIResponse):
            city_details_response = city_details.agent_response
        
        # Parsear los detalles obtenidos de la ciudad
        places_to_visit, hotels, restaurants = extract_details_from_city_response(city_details_response)
        
        # Reservar vuelo o bus si es el primer día
        if i == 0:
            if current_budget > 200:
                flight_reservation = reserve_flight(date_str=current_date.strftime('%Y-%m-%d'), departure="La Paz", destination=city)
                current_budget -= flight_reservation.cost
                itinerary.append(f"Vuelo hacia {city} el {current_date.strftime('%Y-%m-%d')}, Costo: {flight_reservation.cost}")
            else:
                bus_reservation = reserve_bus(date_str=current_date.strftime('%Y-%m-%d'), departure="Oruro", destination=city)
                current_budget -= bus_reservation.cost
                itinerary.append(f"Bus hacia {city} el {current_date.strftime('%Y-%m-%d')}, Costo: {bus_reservation.cost}")
        
        # Reservar hotel si hay disponibilidad y presupuesto
        if hotels and current_budget > 100:
            hotel_name = hotels[0]  # Tomar el primer hotel recomendado
            hotel_reservation = reserve_hotel(
                checkin_date_str=current_date.strftime('%Y-%m-%d'), 
                checkout_date_str=(current_date + timedelta(days=1)).strftime('%Y-%m-%d'),
                hotel_name=hotel_name, 
                city=city
            )
            current_budget -= hotel_reservation.cost
            itinerary.append(f"Hotel en {city} ({hotel_name}) del {current_date.strftime('%Y-%m-%d')}, Costo: {hotel_reservation.cost}")
        
        # Reservar restaurante si hay disponibilidad y presupuesto
        if restaurants and current_budget > 20:
            restaurant_name = restaurants[0]  # Tomar el primer restaurante recomendado
            restaurant_reservation = reserve_restaurant(
                reservation_time_str=(current_date + timedelta(hours=20)).strftime('%Y-%m-%d'),
                restaurant=restaurant_name,
                city=city,
                dish="Especialidad del chef"
            )
            current_budget -= restaurant_reservation.cost
            itinerary.append(f"Restaurante en {city} ({restaurant_name}) el {current_date.strftime('%Y-%m-%d')}, Costo: {restaurant_reservation.cost}")
        
        # Revisar el presupuesto restante
        if current_budget < 50:
            break  # Si el presupuesto restante es menor a 50 USD, detener el itinerario
    
    # Retornar el itinerario y el costo total
    total_cost = budget - current_budget
    return {
        "itinerary": itinerary,
        "total_cost": total_cost,
        "remaining_budget": current_budget
    }

def extract_cities_from_response(response: str) -> list:
    """
    Extrae las ciudades del TravelGuideRAG response.
    """
    # Supongamos que el response es una lista de ciudades
    cities = []
    lines = response.splitlines()
    for line in lines:
        if "Ciudad" in line:
            cities.append(line.split(":")[1].strip())
    return cities

def extract_details_from_city_response(response: str) -> tuple:
    """
    Extrae lugares de interés, hoteles y restaurantes del TravelGuideRAG response.
    """
    places_to_visit = []
    hotels = []
    restaurants = []
    
    lines = response.splitlines()
    current_section = None
    
    for line in lines:
        if "Places to Visit" in line:
            current_section = "places"
        elif "Hotels" in line:
            current_section = "hotels"
        elif "Restaurants" in line:
            current_section = "restaurants"
        elif current_section == "places" and line.strip():
            places_to_visit.append(line.strip())
        elif current_section == "hotels" and line.strip():
            hotels.append(line.strip())
        elif current_section == "restaurants" and line.strip():
            restaurants.append(line.strip())
    
    return places_to_visit, hotels, restaurants


flight_tool = FunctionTool.from_defaults(fn=reserve_flight, return_direct=False)
bus_tool = FunctionTool.from_defaults(fn=reserve_bus, return_direct=False)
hotel_tool = FunctionTool.from_defaults(fn=reserve_hotel, return_direct=False)
restaurant_tool = FunctionTool.from_defaults(fn=reserve_restaurant, return_direct=False)
trip_summary_tool = FunctionTool.from_defaults(fn=generate_trip_summary, return_direct=False)
trip_planner_tool = FunctionTool.from_defaults(fn=generate_itinerary, return_direct=False)