from datetime import datetime
from stackapi import StackAPI
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la API para obtener preguntas y respuestas
SITE = StackAPI('stackoverflow')
response = SITE.fetch('questions', filter='withbody')

# Iterar sobre las preguntas
for question in response.get('items', []):
    question_id = question.get('question_id')
    question_creation_date = question.get('creation_date')  # Fecha en timestamp
    
    # Si la pregunta está contestada, obtenemos las respuestas
    if question.get('is_answered'):
        answers = SITE.fetch('questions/{}/answers'.format(question_id), filter='withbody')
        
        # Buscar la respuesta aceptada
        for answer in answers.get('items', []):
            if answer.get('is_accepted'):
                answer_creation_date = answer.get('creation_date')  # Fecha de la respuesta en timestamp
                
                # Convertir timestamps a datetime para calcular la diferencia
                question_time = datetime.fromtimestamp(question_creation_date)
                answer_time = datetime.fromtimestamp(answer_creation_date)
                time_difference = answer_time - question_time

                print(f"Pregunta ID: {question_id}")
                print(f"Diferencia de tiempo: {time_difference}")
                break  # Detenemos el bucle al encontrar la respuesta aceptada

# Lista para almacenar tiempos de respuesta
response_times = []

# Código para obtener tiempos de respuesta aquí (como el ejemplo previo)
# Y luego añade cada `time_difference` a la lista en segundos, minutos, o el formato que prefieras:
response_times.append(time_difference.total_seconds() / 60)  # Tiempo en minutos

# Calcular estadísticas básicas
avg_time = np.mean(response_times)
median_time = np.median(response_times)
print(f"Tiempo promedio: {avg_time} minutos")
print(f"Mediana del tiempo de respuesta: {median_time} minutos")

# Crear un histograma
plt.hist(response_times, bins=30)
plt.title("Distribución de tiempos de respuesta (en minutos)")
plt.xlabel("Tiempo de respuesta (minutos)")
plt.ylabel("Frecuencia")
plt.show()