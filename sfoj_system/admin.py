from django.contrib import admin
from .models import Board, Judge_State, Users, Code_History

# Register your models here.
admin.site.register(Board)
admin.site.register(Judge_State)
admin.site.register(Users)
admin.site.register(Code_History)