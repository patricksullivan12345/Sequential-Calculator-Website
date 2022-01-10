from django.urls import path
from . import CRUD_views, CALC_views

urlpatterns = [ #Use kwargs when finding the url path in runserver

    path('', CRUD_views.list_projects, name="projects"),
    path('project/<str:pk>/', CALC_views.relationship_queries, name='project'),

    path('create-project/', CRUD_views.createProject, name="create-project"),
    path('create-fiber/<str:pk>/', CRUD_views.createFiber, name="create-fiber"),
    path('create-seq/<str:pk>/', CRUD_views.createSeq, name="create-seq"),
    path('seq-redirect/<str:pk>/', CRUD_views.redirectSeq, name="seq-redirect"),

    path('update-project/<str:pk>/', CRUD_views.updateProject, name='update-project'),
    path('update-fiber/<str:pk>/', CRUD_views.updateFiber, name="update-fiber"),
    path('update-seq/<str:pk>/', CRUD_views.updateSeq, name="update-seq"),

    path('delete-seq/<str:pk>/', CRUD_views.deleteSeq, name="delete-seq"),
    path('delete-fiber/<str:pk>/', CRUD_views.deleteFiber, name="delete-fiber"),
    path('delete-project/<str:pk>/', CRUD_views.deleteProject, name='delete-project'),

]