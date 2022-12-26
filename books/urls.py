from django.urls import path
from . import views
from graphene_django.views import GraphQLView
from books.schema import schema


urlpatterns = [
    path('', views.home, name='home'),
    # Only single URL to access GraphQL this is single end point from where we can access all the queries
    path('graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
    # the GraphQLView class is to give graphical interface to do query
]