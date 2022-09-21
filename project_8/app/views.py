from django.shortcuts import render

# Create your views here.
def index(request, groupname):
    template_name = 'app/index.html'
    return render(request, template_name, {'group_name':groupname})