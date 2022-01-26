from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.tool_list, name='tool_list'),
    path('<slug:keeper_slug>/', views.tool_list,
         name='tool_list_by_keeper'),
    path('<slug:keeper_slug>/operations', views.keeper_operations,
         name='keeper_operations_list'),

    path('<int:id>/<slug:slug>/', views.tool_detail,
         name='tool_detail'),
    path('<int:id>/<slug:slug>/oper/', views.tool_operation,
         name='tool_operation'),
]