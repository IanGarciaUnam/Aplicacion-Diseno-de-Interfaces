from django.shortcuts import render
import requests

# Create your views here.
def index(request):
  # Obtenemos la lista de cosas por hacer
  response = requests.get('https://jsonplaceholder.typicode.com/todos/')
  # Tranformamos la respuesta en un objeto JSON
  todos = response.json()
  return render(request, "main_app/home.html", {"todos": todos})