#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
User = get_user_model()
from django.contrib.sessions.backends.db import SessionStore

from .base import FunctionalTest


class MyListTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## 쿠키를 설정하기 위해 도메인 접속이 필요하다
        ## 404 페이지가 뜬다.
        self.browser.get(self.server_url + '/404_no_such_url')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))
        
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'gulby@example.com'
        
        self.browser.get(self.server_url)
        self.wait_to_be_logged_out(email)
        
        # 굴비가 사용자로 로그인한다.
        self.create_pre_authenticated_session(email)
        
        self.browser.get(self.server_url)
        self.wait_to_be_logged_in(email)
        
    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # 에디스가 사용자로 로그인한다.
        self.create_pre_authenticated_session('edith@example.com')
        
        # 메인페이지로 가서 목록 입력을 시작한다.
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('그물 만들기\n')
        self.get_item_input_box().send_keys('쇼핑하기\n')
        first_list_url = self.browser.current_url
        
        # 첫번째 아이템을 위한 "나의 목록" 링크를 발견한다.
        self.browser.find_element_by_link_text('나의 목록').click()
        #self.assertNotEqual(first_list_url, self.browser.current_url)
        
        # 그녀가 만든 목록에 첫번째 아이템이 있는 것을 확인한다.
        self.browser.find_element_by_link_text('그물 만들기')
        self.assertEqual(self.browser.current_url, first_list_url)
        
        # 다른 목록도 확인하기도 한다.
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('게임하기\n')
        second_list_url = self.browser.current_url
        
        # "나의 목록" 아래에 새로운 목록이 표시된다.
        self.browser.find_element_by_link_text('나의 목록').click()
        self.assertNotEqual(first_list_url, self.browser.current_url)
        self.get_item_input_box().send_keys('게임하기').click()
        self.assertEqual(self.browser.current_url, second_list_url)
        
        # 로그아웃한다. "나의 목록" 옵션이 사라진다.
        self.browser.find_element_by_id('id_logout').click()
        self.assertEqual(
            self.browser.find_elements_by_link_text('나의 목록'),
            []
        )
        