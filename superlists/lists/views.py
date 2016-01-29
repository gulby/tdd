#-*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError

from lists.models import Item, List

# Create your views here.
def home_page(request):
    items = Item.objects.all()
    return render(request, 'home.html')
    
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'list': list_})
    
def new_list(request):
    list_ = List.objects.create()
    new_item_text = request.POST.get('item_text')
    item = Item(text=new_item_text, list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = u'빈 아이템을 등록할 수 없습니다'
        return render(request, 'home.html', {'error': error})
    return redirect('/lists/%d/' % (list_.id,))

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    new_item_text = request.POST.get('item_text')
    new_item = Item.objects.create(text=new_item_text, list=list_)
    return redirect('/lists/%d/' % (list_.id,))