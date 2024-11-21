import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import matplotlib.pyplot as plt
import textstat

# Leer el JSON de preguntas desde un archivo
with open('questions.json', 'r', encoding='utf-8') as file:
    questions_json = json.load(file)

# Filtrar preguntas que han sido respondidas correctamente
answered_questions = [q for q in questions_json["items"] if q.get("is_answered")]

# Inicializar listas para las gráficas y cálculos
time_differences = []
legibility_scores = []
question_ids = []

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
            time_difference = (answer_time - question_time).total_seconds() / 3600  # En horas
            time_differences.append(time_difference)
            question_ids.append(question_id)

            # Calcular métrica de legibilidad
            legibility_score = textstat.flesch_reading_ease(answer_text)
            legibility_scores.append(legibility_score)

            # Mostrar resultados
            print(f"Pregunta ID: {question_id}")
            print(f"Link: {question_link}")
            print(f"Texto de la respuesta aceptada: {answer_text}")
            print(f"Diferencia de tiempo (horas): {time_difference:.2f}")
            print(f"Flesch Reading Ease: {legibility_score:.2f}")
            print("")
    else:
        print(f"Error al acceder a la pregunta: {question_link}")

# Calcular promedios
average_time_difference = sum(time_differences) / len(time_differences) if time_differences else 0
average_legibility_score = sum(legibility_scores) / len(legibility_scores) if legibility_scores else 0

# Mostrar promedios
print(f"Promedio de diferencia de tiempo (horas): {average_time_difference:.2f}")
print(f"Promedio de legibilidad (Flesch Reading Ease): {average_legibility_score:.2f}")

# Graficar los resultados
plt.figure(figsize=(12, 6))

# Gráfica de diferencias de tiempo
plt.bar(question_ids, time_differences, color='skyblue', label='Diferencia de tiempo (horas)')
plt.axhline(y=average_time_difference, color='r', linestyle='--', label='Promedio de tiempo')
plt.xlabel('ID de la Pregunta')
plt.ylabel('Diferencia de Tiempo (horas)')
plt.title('Tiempo de Respuesta por Pregunta')
plt.legend()
plt.show()

# Gráfica de legibilidad
plt.figure(figsize=(12, 6))
plt.bar(question_ids, legibility_scores, color='lightgreen', label='Legibilidad (Flesch Reading Ease)')
plt.axhline(y=average_legibility_score, color='r', linestyle='--', label='Promedio de legibilidad')
plt.xlabel('ID de la Pregunta')
plt.ylabel('Legibilidad (Flesch Reading Ease)')
plt.title('Legibilidad de Respuestas por Pregunta')
plt.legend()
plt.show()
