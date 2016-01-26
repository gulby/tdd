#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()
        
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        #에디스는 멋진 작업 목록 온라인 앱이 나왔다는 소식을 듣고
        #해당 웹사이트를 확인하러 갔다.
        self.browser.get('http://localhost:8000')
        
        # 웹 페이지 타이틀과 헤더가 'To-Do'를 표시하고 있다.
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        # 그녀는 바로 작업을 추가하기로 한다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            u'작업 아이템 입력',
        )
        
        # "공작깃털 사기" 라고 텍스트 상자에 입력한다.
        # (에디스의 취미는 날치 잡이용 그물을 만드는 것이다)
        input1 = u'공작깃털 사기'
        inputbox.send_keys(input1)
        
        # 엔터키를 치면 페이지가 갱신되고 작업 목록에
        # "1: 공작깃털 사기" 아이템이 추가된다.
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: %s' % input1)
        
        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자가 존재한다.
        # 다시 "공작깃털을 이용해서 그물 만들기" 라고 입력한다 (에디스는 매우 체계적인 사람이다)
        inputbox = self.browser.find_element_by_id('id_new_item')
        input2 = u'공작깃털을 이용해서 그물 만들기'
        inputbox.send_keys(input2)
        inputbox.send_keys(Keys.ENTER)
        
        # 페이지는 다시 갱신되고, 두 개 아이템이 목록에 보인다.
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_list_table('1: %s' % input1)
        self.check_for_row_in_list_table('2: %s' % input2)
        
        # 에디스는 사이트가 입력한 목록을 저장하고 있는지 궁금하다.
        # 사이트는 그녀를 위한 특정 URL 을 생성해준다.
        # 이때 URL 에 대한 설명도 제공된다.
        self.fail('Finish the test!')
        
        # 해당 URL 에 접속하면 그녀가 만든 작업 목록이 그대로 있는 것을 확인할 수 있다.
        
        # 만족하고 잠자리에 든다.

if __name__ == '__main__':
    unittest.main()
