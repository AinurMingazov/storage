from django.urls import path
from store.views import *
from django.views.decorators.cache import cache_page

app_name = 'store'

urlpatterns = [
    path('', tool_list, name='tool_list'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('logout/', logout_user, name='logout'),
    path('<slug:keeper_slug>/', tool_list, name='tool_list_by_keeper'),
    # path('operations/<slug:keeper_slug>/', cache_page(60)(KeeperOperations.as_view()), name='keeper_operations_list'),
    path('operations/<slug:keeper_slug>/', KeeperOperations.as_view(), name='keeper_operations_list'),
    path('tool/<int:pk>/', ToolDetail.as_view(), name='tool_detail'),
    path('oper/<int:id>/', tool_operation, name='tool_operation'),



]