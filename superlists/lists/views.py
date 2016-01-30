#-*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from django.views.generic import FormView, CreateView, DetailView
#from django.views.generic.detail import SingleObjectMixin

from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm

# Create your views here.
class HomePageView(FormView):
    template_name = 'home.html'
    form_class = ItemForm
    
class ViewAndAddToList(CreateView, DetailView):
    model = List
    template_name = 'list.html'
    form_class = ExistingListItemForm
    
    def get_form(self, form_class=ExistingListItemForm):
        self.object = self.get_object()
        return form_class(for_list=self.get_object(), data=self.request.POST)
    
class NewListView(CreateView):
    form_class = ItemForm
    template_name = 'home.html'
    
    def form_valid(self, form):
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)