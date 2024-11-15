import requests
from stackapi import StackAPI
SITE = StackAPI('stackoverflow')
response = SITE.fetch('answers')

questions = response.get('items', [])

# Iterar sobre las preguntas y extraer información específica
for question in questions:
    question_id = question.get('question_id')
    answer_id = question.get('answer_id')
    is_accepted = question.get('is_accepted')
    score = question.get('score')
    creation_date = question.get('creation_date')

    # Guardar estos datos en variables o imprimirlos
    if is_accepted == True:
        print(f"IDquestion: {question_id}\n IDanswer: {answer_id}\n Respondida: {is_accepted}\n Score: {score}\n Respuestas: {creation_date}")
        print("")
