from django.urls import path
from store.views import *

app_name = 'store'

urlpatterns = [
    path('', tool_list, name='tool_list'),
    path('<slug:keeper_slug>/', tool_list, name='tool_list_by_keeper'),
    path('operations/<slug:keeper_slug>/', KeeperOperations.as_view(), name='keeper_operations_list'),
    path('tool/<int:pk>/', ToolDetail.as_view(), name='tool_detail'),
    path('oper/<int:id>/', tool_operation, name='tool_operation'),
]