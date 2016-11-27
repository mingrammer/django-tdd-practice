from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith go main page and will add empty item by mistake
        # Press enter key when input box is empty
        self.browser.get(self.server_url)
        self.get_item_input_box().send_keys('\n')

        # Page is reloaded and show error message that can not add empty item
        error = self.browser.find_element_by_css_selector('.has-error')

        self.assertEqual(error.text, 'You can\'t have an empty list item')

        # Typing other item is processed correctly
        self.get_item_input_box().send_keys('Buy milk\n')
        self.check_for_row_in_list_table('1: Buy milk')

        # She add empty item again intentionally
        self.get_item_input_box().send_keys('\n')

        # Error message is shown again in list page
        self.check_for_row_in_list_table('1: Buy milk')

        error = self.browser.find_element_by_css_selector('.has-error')

        self.assertEqual(error.text, 'You can\'t have an empty list item')

        # Register non-empty item is valid
        self.get_item_input_box().send_keys('Make tea\n')
        self.check_for_row_in_list_table('1: Buy milk')
        self.check_for_row_in_list_table('2: Make tea')
