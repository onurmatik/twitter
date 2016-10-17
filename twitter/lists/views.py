from django.shortcuts import render
from django.views.generic import CreateView
from twitter.lists.models import List


class ListCreateView(CreateView):
    model = List
