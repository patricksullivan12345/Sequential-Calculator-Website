from django.urls import path
from . import views

urlpatterns = [ #Use kwargs when finding the url path in runserver

    path('', views.list_projects, name="projects"),
    path('project/<str:pk>/', views.relationship_queries, name='project'),

    path('create-project/', views.createProject, name="create-project"),
    path('create-fiber/<str:pk>/', views.createFiber, name="create-fiber"),
    path('create-seq/<str:pk>/', views.createSeq, name="create-seq"),
    path('seq-redirect/<str:pk>/', views.redirectSeq, name="seq-redirect"),

    path('update-project/<str:pk>/', views.updateProject, name='update-project'),
    path('update-fiber/<str:pk>/', views.updateFiber, name="update-fiber"),
    path('update-seq/<str:pk>/', views.updateSeq, name="update-seq"),

    path('delete-seq/<str:pk>/', views.deleteSeq, name="delete-seq"),
    path('delete-fiber/<str:pk>/', views.deleteFiber, name="delete-fiber"),
    path('delete-project/<str:pk>/', views.deleteProject, name='delete-project'),

]