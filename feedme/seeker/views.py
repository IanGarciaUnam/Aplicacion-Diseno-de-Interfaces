from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
  template_name='index.html'
  
def index(request):
  return render(request, 'seeker/index.html', {})
  # return HttpResponse("Hello, world. You're at the polls index.")
