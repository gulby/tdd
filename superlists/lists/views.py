#-*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from django.views.generic import FormView, CreateView, DetailView
from django.views.generic.detail import SingleObjectMixin

from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm, EMPTY_LIST_ERROR


# Create your views here.
class HomePageView(FormView):
    template_name = 'home.html'
    form_class = ItemForm
    
class ViewAndAddToList(CreateView, SingleObjectMixin):
    model = List
    template_name = 'list.html'
    form_class = ExistingListItemForm
    
    def get_form(self, form_class=ExistingListItemForm):
        self.object = self.get_object()
        return form_class(for_list=self.get_object(), data=self.request.POST)
        
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})
    
class NewListView(CreateView):
    form_class = ItemForm
    template_name = 'home.html'
    
    def form_valid(self, form):
        list_ = List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)

def my_lists(request, email):
    return render(request, 'my_lists.html')
    