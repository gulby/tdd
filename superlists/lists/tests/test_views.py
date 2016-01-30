#-*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_LIST_ERROR, DUPLICATE_ITEM_ERROR, ExistingListItemForm


class HomePageTest(TestCase):
        
    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
        
    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other itemey 3', list=other_list)
        Item.objects.create(text='other itemey 4', list=other_list)
        
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other itemey 3')
        self.assertNotContains(response, 'other itemey 4')
        self.assertTemplateUsed(response, 'list.html')
        
    def test_can_save_a_POST_request(self):
        input1 = u'신규 작업 아이템'
        self.client.post(
            '/lists/new',
            data={'text': input1}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, input1)
        
    def test_redirects_after_POST(self):
        input1 = u'신규 작업 아이템'
        response = self.client.post(
            '/lists/new',
            data={'text': input1}
        )
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
        
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.assertEqual(correct_list, List.objects.get(id=correct_list.id))
        
        response = self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': u'기존 목록에 신규 아이템'},
        )
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
        
        self.assertEqual(Item.objects.count(), 1, 'count is not 1: %d' % Item.objects.count())
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, u'기존 목록에 신규 아이템')
        self.assertEqual(new_item.list, correct_list)
        
    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': u'기존 목록에 신규 아이템'},
        )
        
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
        
    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            '/lists/%d/' % (list_.id,),
            data={'text': ''}
        )
        
    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)
        
    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertTemplateUsed(response, 'list.html')
        
    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        
    def test_for_invalid_input_shows_error_on_page(self):
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_LIST_ERROR))
        
    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')
        
    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='textey')
        response = self.client.post(
            '/lists/%d/' % (list1.id,),
            data={'text': 'textey'}
        )
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, 'list.html')
        self.assertEqual(Item.objects.all().count(), 1)


class NewListTest(TestCase):

    response = None

    def setUp(self):
        self.response = self.client.post('/lists/new', data={'text': ''})
        
    def tearDown(self):
        pass

    def test_invalid_list_items_arent_saved(self):
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
        
    def test_for_invalid_input_status(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_for_invalid_input_renders_home_template(self):
        self.assertTemplateUsed(self.response, 'home.html')
        
    def test_validation_errors_are_shown_on_home_page(self):
        self.assertContains(self.response, escape(EMPTY_LIST_ERROR))
        
    def test_for_invalid_input_passes_form_to_template(self):
        self.assertIsInstance(self.response.context['form'], ItemForm)