from django.shortcuts import render
from .models import Chat, Group
# Create your views here.
def index(request, groupname):
    template_name = 'app/index.html'
    group = Group.objects.filter(name=groupname).first()
    chat = []
    if group:
        chat = Chat.objects.filter(group=group)
    else:
        group_crate = Group(name=groupname)
        group_crate.save()
    return render(request, template_name, {'group_name':groupname, 'chats':chat})