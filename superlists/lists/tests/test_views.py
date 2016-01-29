#-*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        
        self.assertEqual(found.func, home_page)
        
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        
        expected_html = render_to_string('home.html')
        
        self.assertEqual(response.content.decode('utf8'), expected_html)


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
            data={'item_text': input1}
        )
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, input1)
        
    def test_redirects_after_POST(self):
        input1 = u'신규 작업 아이템'
        response = self.client.post(
            '/lists/new',
            data={'item_text': input1}
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
            data={'item_text': u'기존 목록에 신규 아이템'},
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
            data={'item_text': u'기존 목록에 신규 아이템'},
        )
        
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))


class NewListTest(TestCase):

    def test_validation_errors_are_sent_back_to_hame_page_template(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape(u'빈 아이템을 등록할 수 없습니다')
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
        