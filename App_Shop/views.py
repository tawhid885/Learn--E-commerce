from django.shortcuts import render


#Models
from .models import Category, Product

#Views
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin



class Home(ListView):
    model = Product
    template_name = 'App_Shop/home.html'

class ProductDetail(DetailView,LoginRequiredMixin):
    model = Product
    template_name = "App_Shop/product_detail.html"


