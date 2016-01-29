#-*- coding: utf-8 -*-
from django import forms

from lists.models import Item

EMPTY_LIST_ERROR = u'빈 아이템을 등록할 수 없습니다'


class ItemForm(forms.models.ModelForm):
    
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': u'작업 아이템 입력',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_LIST_ERROR}
        }
    
    def save(self, for_list):
        self.instance.list = for_list
        return super(ItemForm, self).save()
        