from llama_index.core import PromptTemplate

travel_guide_description = """
Herramienta de guía de viajes para Bolivia. Esta herramienta proporciona información útil y recomendaciones sobre lugares turísticos, actividades, restaurantes, y hoteles en distintas ciudades bolivianas.
- Parámetros de entrada: Pregunta o consulta sobre una ciudad o actividad turística.
- Salida: Información detallada y recomendaciones personalizadas para la consulta realizada.
"""

travel_guide_qa_str = """
==> COMPLETE PROMPT TEMPLATE HERE <===
"""

agent_prompt_str = """
==> COMPLETE PROMPT TEMPLATE HERE <===
"""

travel_guide_qa_tpl = PromptTemplate(travel_guide_qa_str)
agent_prompt_tpl = PromptTemplate(agent_prompt_str)
