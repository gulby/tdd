#-*- coding: utf-8 -*-
from django.test import TestCase

from lists.forms import ItemForm


class ItemFormTest(TestCase):

    def test_form_item_input_has_placeholder_and_css_classes(self):
        form = ItemForm()
        self.assertIn(u'placeholder="작업 아이템 입력"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())
        