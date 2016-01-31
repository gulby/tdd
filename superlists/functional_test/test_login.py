#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import time

from .base import FunctionalTest
from selenium.webdriver.support.ui import WebDriverWait


class LoginTest(FunctionalTest):

    def switch_to_new_window(self, text_in_title):
        retries = 50
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
            time.sleep(0.2)
        self.fail('창을 찾을 수 없습니다')
        
    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=10).until(
            lambda b: b.find_element_by_id(element_id)
        )

    def test_login_with_persona(self):
        # 에디스는 superlist 사이트에 접속한다.
        # 그리고 "로그인" 링크를 발견한다.
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('login').click()
        
        # 개인 로그인 박스가 표시된다.
        self.switch_to_new_window('Mozilla Persona')
        
        # 에디스는 이메일 주소를 이용해서 로그인한다.
        ## 테스트 이메일로 mockmyid.com 사용
        self.browser.find_element_by_id(
            'authentication_email'
        ).send_keys('gulby@mockmyid.com')
        self.browser.find_element_by_tag_name('button').click()
        
        # 개인 창을 닫는다.
        self.switch_to_new_window('To-Do')
        
        # 로그인된 것을 알 수 있다.
        self.wait_for_element_with_id('logout')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn('gulby@mockmyid.com', navbar.text)
        