from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith go main page and will add empty item by mistake
        # Press enter key when input box is empty

        # Page is reloaded and show error message that can not add empty item

        # Typing other item is processed correctly

        # She add empty item again intentionally

        # Error message is shown again in list page

        self.fail('Write me!')
