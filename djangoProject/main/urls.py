from django.urls import path
from . import views

urlpatterns = [
        path('auth/', views.AuthAPIView.as_view()),

        path('tasks/', views.TasksApiView.as_view()),
        path('tasks_cassifier/', views.TaskTypeApiView.as_view()),
        path('tasks_priority/', views.TaskPriorityApiView.as_view()),
        path('employees/', views.EmlpoyeeApiView.as_view()),
        path('contracts/', views.ContractApiView.as_view()),
        path('users/', views.UserApiView.as_view()),
        path('contact_numbers/', views.ContactPersonAPIView.as_view()),
        path('organization/', views.OrganizationAPIView.as_view())
]
