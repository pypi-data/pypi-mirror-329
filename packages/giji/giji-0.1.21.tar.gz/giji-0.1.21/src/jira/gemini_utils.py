"""Gemini utilities for Jira integration"""

import google.generativeai as genai
from typing import Optional


def generate_jira_comment(pr_summary: str, jira_description: str, api_key: str) -> str:
    """Generate a Jira comment explaining the implemented changes"""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Actúa como un experto desarrollador explicando los cambios técnicos realizados en un Pull Request.
    
    Reglas importantes y ESTRICTAS:
    1. SOLO mencionar archivos y cambios que estén EXPLÍCITAMENTE listados en el PR summary proporcionado
    2. NO inventar o inferir cambios adicionales que no estén en el PR summary
    3. NO mencionar archivos que no aparezcan en el PR summary
    4. Explicar de manera técnica y precisa ÚNICAMENTE los cambios implementados que se muestran
    5. Ser conciso y directo, enfocándose solo en lo que realmente se cambió
    
    Formato del comentario:
    
    ## Cambios Implementados
    
    • [Archivo mencionado en PR]: [Descripción técnica de SOLO los cambios mostrados]
    • [Siguiente archivo mencionado...]
    
    ## Detalles Técnicos
    
    [Breve explicación técnica basada ÚNICAMENTE en los cambios mostrados]
    
    Cambios a explicar (USAR SOLO ESTOS CAMBIOS, NO AGREGAR OTROS):
    {pr_summary}
    """

    generation_config = {
        "temperature": 0.3,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    response = model.generate_content(
        prompt, generation_config=generation_config, safety_settings=safety_settings
    )

    return response.text 