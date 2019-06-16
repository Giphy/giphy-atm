import requests
import sys


query = sys.argv[0]

print("OLD MODEL:\n")
r = requests.get('http://localhost:9000/poem_old?query={}'.format(query))
poem = r.json()['data']
print(poem)

print("\nNEW MODEL:\n")
r = requests.get('http://localhost:9000/poem?query={}'.format(query))
poem = r.json()['data']
print(poem)