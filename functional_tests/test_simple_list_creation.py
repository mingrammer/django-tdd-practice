from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.server_url)

        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Type the task
        inputbox = self.browser.find_element_by_id('id_new_item')

        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Type task item'
        )

        # The page will be reloaded when 'enter' is pressed
        # Task will be added to list
        inputbox.send_keys('Buy a bike')
        inputbox.send_keys(Keys.ENTER)

        # Virtual user : edith
        edith_list_url = self.browser.current_url

        self.assertRegex(edith_list_url, '/lists/.+')

        self.check_for_row_in_list_table('1: Buy a bike')

        # There is additional text box to add a item
        # Type the other task
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy a car')
        inputbox.send_keys(Keys.ENTER)

        # The page will be reloaded again
        # There are two items in list
        self.check_for_row_in_list_table('1: Buy a bike')
        self.check_for_row_in_list_table('2: Buy a car')

        # New virtual user entered site

        # prevents the inflowing the edith's information through cookie
        # using browser session.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.server_url)

        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn('Buy a bike', page_text)
        self.assertNotIn('Buy a car', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Virtual use : francis
        francis_list_url = self.browser.current_url

        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Check there is no edith's inputs
        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn('Buy a bike', page_text)
        self.assertIn('Buy milk', page_text)
