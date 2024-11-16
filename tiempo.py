import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Leer el JSON de preguntas desde un archivo
with open('questions.json', 'r') as file:
    questions_json = json.load(file)

# Filtrar preguntas que han sido respondidas correctamente
answered_questions = [q for q in questions_json["items"] if q.get("is_answered")]
# Iterar sobre las preguntas filtradas
for question in answered_questions:
    question_id = question.get("question_id")
    question_link = question.get("link")
    question_creation_date = question.get("creation_date")
    
    # Scraping de la página de la pregunta
    response = requests.get(question_link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Buscar la respuesta aceptada
        accepted_answer = soup.find('div', class_='answer js-answer accepted-answer js-accepted-answer')
        if accepted_answer:
            # Obtener el texto de la respuesta aceptada
            answer_text = accepted_answer.find('div', class_='js-post-body')
            paragraphs = [p.get_text(strip=True) for p in answer_text.find_all('p')]
            answer_text = " ".join(paragraphs)

            # Obtener la fecha de creación de la respuesta aceptada (desde el atributo data-value)
            answer_creation_date = accepted_answer.find('time')['datetime']
            answer_time = datetime.strptime(answer_creation_date, '%Y-%m-%dT%H:%M:%S')

            # Convertir la fecha de creación de la pregunta a formato datetime
            question_time = datetime.fromtimestamp(question_creation_date)

            # Calcular diferencia de tiempo
            time_difference = answer_time - question_time

            # Mostrar resultados
            print(f"Pregunta ID: {question_id}")
            print(f"Link: {question_link}")
            print(f"Texto de la respuesta aceptada: {answer_text}")
            print(f"Diferencia de tiempo: {time_difference}")
            print("")
            print("")
    else:
        print(f"Error al acceder a la pregunta: {question_link}")
