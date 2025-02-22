from django.http import HttpResponse
from django.shortcuts import render, redirect
from investor.models import investment_data  # Importing from investor app
from entrepreneur.models import entrepreneur_data  # Importing from entrepreneur app
from django.contrib.auth.hashers import check_password
from django.contrib import messages

def home(request):
    
# Create your views here.
