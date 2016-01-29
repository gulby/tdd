#-*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError

from lists.models import Item, List
from lists.forms import ItemForm

# Create your views here.
def home_page(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'form': ItemForm()})
    
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    
    if request.method == 'POST':
        try:
            new_text = request.POST['text']
            new_item = Item(text=new_text, list=list_)
            new_item.full_clean()
            new_item.save()
            return redirect('/lists/%d/' % (list_.id,))
        except ValidationError:
            error = u'빈 아이템을 등록할 수 없습니다'
            
    return render(request, 'list.html', {'list': list_, 'error': error})
    
def new_list(request):
    list_ = List.objects.create()
    new_text = request.POST.get('text')
    item = Item(text=new_text, list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = u'빈 아이템을 등록할 수 없습니다'
        return render(request, 'home.html', {'error': error})
    return redirect(list_)
