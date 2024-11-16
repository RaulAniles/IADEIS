import requests

url = 'https://magicloops.dev/api/loop/4bf3b75f-8167-4586-abc2-052363f8874c/run'
payload = { 'input': 'I love Magic Loops!' }

response = requests.get(url, json=payload)
responseJson = response.json()
print(responseJson)