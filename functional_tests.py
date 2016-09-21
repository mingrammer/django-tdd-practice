from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # Type the task

        # The page will be reloaded when 'enter' is pressed
        # Task will be added to list

        # There is additional text box to add a item
        # Type the other task

        # The page will be reloaded again
        # There are two items in list
        # Generate url for the task list
        # The url should has description

        # When a user access to the url, he/she can view the task list


if __name__ == '__main__':
    unittest.main(warnings='ignore')
