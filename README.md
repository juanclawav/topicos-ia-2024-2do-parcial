
# Asistente de Viajes
=====================================

Este proyecto es un asistente de viajes que utiliza inteligencia artificial para planificar y gestionar viajes de turismo en Bolivia. El asistente tiene acceso a diversas fuentes de información sobre atracciones turísticas bolivianas y herramientas para reservar vuelos, hoteles, restaurantes y actividades.

## Funcionalidades
Recomendaciones de lugares a visitar en una ciudad determinada
Recomendaciones de hoteles y restaurantes
Reserva de vuelos, hoteles y restaurantes
Reporte detallado del viaje
## Endpoints
```
/recommendations/cities: Recomendaciones de lugares a visitar en una ciudad determinada

/recommendations/hotels: Recomendaciones de hoteles

/recommendations/restaurants: Recomendaciones de restaurantes

/reserve/flight: Reserva de vuelos

/reserve/hotel: Reserva de hoteles

/reserve/restaurant: Reserva de restaurantes

/trip/report: Reporte detallado del viaje
```
## Chatbot
El asistente tiene una interfaz de chatbot que permite a los usuarios interactuar con él de manera natural. El chatbot utiliza un modelo de lenguaje para entender las preguntas y proporcionar respuestas relevantes.

### Prompts
Los prompts son descripciones detalladas de las herramientas y funcionalidades del asistente. Los prompts se utilizan para ayudar al modelo de lenguaje a entender las preguntas y proporcionar respuestas relevantes.

## Instrucciones de uso
Clona el repositorio y ejecuta los comandos, para activar el acceso a la API y a la interfaz Chatbot
```
fastapi dev
ai_assistant/api.py
```
Utiliza la interfaz de chatbot para interactuar con el asistente.
Puedes utilizar los endpoints para obtener recomendaciones, reservar vuelos, hoteles y restaurantes, y obtener un reporte detallado del viaje.

```
  {
    "trip_type": "FLIGHT",
    "date": "2023-12-05",
    "departure": "Oruro",
    "destination": "Cochabamba",
    "cost": 554,
    "reservation_type": "TripReservation"
  },
  {
    "checkin_date": "2023-12-05",
    "checkout_date": "2023-12-15",
    "hotel_name": "El Lucero",
    "city": "Oruro",
    "cost": 990,
    "reservation_type": "HotelReservation"
  },
  {
    "reservation_time": "2023-12-07T20:00:00",
    "restaurant": "Gustu",
    "city": "La Paz",
    "dish": "not specified",
    "cost": 29,
    "reservation_type": "RestaurantReservation"
  },
  {
    "trip_type": "FLIGHT",
    "date": "2024-01-02",
    "departure": "Cochabamba",
    "destination": "Dallas",
    "cost": 401,
    "reservation_type": "TripReservation"
  }
```

