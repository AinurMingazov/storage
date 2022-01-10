from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.tool_list, name='tool_list'),
    path('<slug:keeper_slug>/', views.tool_list,
         name='tool_list_by_keeper'),
    path('<int:id>/<slug:slug>/', views.tool_detail,
         name='tool_detail'),
]