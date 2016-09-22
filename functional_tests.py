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
        self.browser.get('http://localhost:8000')

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

        # There is additional text box to add a item
        # Type the other task
        self.check_for_row_in_list_table('1: Buy a bike')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy a car')
        inputbox.send_keys(Keys.ENTER)

        # The page will be reloaded again
        # There are two items in list
        self.check_for_row_in_list_table('1: Buy a bike')
        self.check_for_row_in_list_table('2: Buy a car')

        inputbox = self.browser.find_element_by_id('id_new_item')

        # Generate url for the task list
        # The url should has description

        self.fail('Finish the test!')
        # When a user access to the url, he/she can view the task list


if __name__ == '__main__':
    unittest.main(warnings='ignore')
