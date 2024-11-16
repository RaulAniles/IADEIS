from stackapi import StackAPI
import pandas as pd
import time
from datetime import datetime

# Configuración inicial
SITE = StackAPI('stackoverflow')  # Especificamos el sitio
SITE.page_size = 50  # Número de resultados por página
SITE.max_pages = 2  # Límite de páginas a extraer (ajustable según tu necesidad)

# Función para convertir timestamp a fecha
def convert_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Variables para almacenar los datos
questions_data = []
answers_data = []

# Extracción de preguntas recientes
print("Extrayendo preguntas...")
questions = SITE.fetch('questions', tagged='python', sort='creation', order='desc')

for question in questions['items']:
    question_id = question['question_id']
    questions_data.append({
        'question_id': question_id,
        'title': question['title'],
        'creation_date': convert_timestamp(question['creation_date']),
        'tags': question['tags'],
        'view_count': question.get('view_count', 0),
        'answer_count': question.get('answer_count', 0),
        'score': question.get('score', 0)
    })

    # Si la pregunta tiene respuestas, extraerlas
    if question['answer_count'] > 0:
        print(f"Extrayendo respuestas de la pregunta {question_id}...")
        answers = SITE.fetch(f'questions/{question_id}/answers', sort='creation')
        for answer in answers['items']:
            answers_data.append({
                'answer_id': answer['answer_id'],
                'question_id': question_id,
                'creation_date': convert_timestamp(answer['creation_date']),
                'score': answer.get('score', 0),
                'is_accepted': answer.get('is_accepted', False),
                'owner_reputation': answer.get('owner', {}).get('reputation', 0),
                'body_length': len(answer.get('body', ''))  # Para medir longitud de la respuesta
            })
    time.sleep(1)
# Convertir los datos a DataFrames para análisis posterior
questions_df = pd.DataFrame(questions_data)
answers_df = pd.DataFrame(answers_data)

# Guardar los resultados en archivos CSV
questions_df.to_csv('questions_data.csv', index=False)
answers_df.to_csv('answers_data.csv', index=False)

print("Datos extraídos y guardados en 'questions_data.csv' y 'answers_data.csv'.")
