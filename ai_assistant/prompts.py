from llama_index.core import PromptTemplate

travel_guide_description = """
Travel Guide RAG is a tool that provides recommendations and answers questions about cities, places, tourist destinations, activities, and attractions in Bolivia.
- Input parameters: Query about tourism in Bolivia, recommendations of cities and places, a city, tourist attraction, or activity.
- Output parameters: The provided output reformulated to fit the users query and answer it accurately using only the information provided.
- Usage: This tool is used to fetch tourist information and offer suggestions to the user. Use only the data provided in the travel guide store.
"""

# Prompt for Travel Guide QA
travel_guide_qa_str = """
Use only the data provided in the context to provide a complete response to the user about tourist destinations, cities, places, activities in Bolivia. If asked about cities only talk about cities.
If given context in a query, make sure to be precise and provide clear details, even if the context is just one word.
Your context may contain information in different languages, but your answer will always be in Spanish. 
If the user asks you about reservations, be sure to use the corresponding tools such as "Flight Tool" for flights, "Hotel Tool" for hotels, "Bus Tool" for buses, and "Restaurant Tool" for restaurants. Make sure to be precise and provide clear details.
Context information is below.
    ---------------------
    {context_str}
    ---------------------
Given the context information and not prior knowledge, provide a response with detailed source information.
User Query: {query}
Response: 
"""

# Main Prompt for the Agent
agent_prompt_str = """
Use only the data provided in the context to provide a complete response to the user about tourist destinations, cities, places, activities in Bolivia. If asked about cities only talk about cities.
If given context in a query, make sure to be precise and provide clear details, even if the context is just one word.
Your context may contain information in different languages, but your answer will always be in Spanish. 
If the user asks you about reservations, be sure to use the corresponding tools such as "Flight Tool" for flights, "Hotel Tool" for hotels, "Bus Tool" for buses, and "Restaurant Tool" for restaurants. Make sure to be precise and provide clear details.
Context information is below.
    ---------------------
    {context_str}
    ---------------------
Given the context information and not prior knowledge, provide a response with detailed source information.
User Query: {query_str}
Response: 
"""


travel_guide_qa_tpl = PromptTemplate(travel_guide_qa_str)
agent_prompt_tpl = PromptTemplate(agent_prompt_str)
