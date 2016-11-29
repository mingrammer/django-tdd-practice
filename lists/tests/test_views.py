import re

from django.test import TestCase
from django.utils.html import escape

from lists.forms import ItemForm
from lists.models import Item, List


class TestCaseWithCSRF(TestCase):
    @staticmethod
    def remove_csrf(html):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html)

    def assertEqualExceptCSRF(self, first, second):
        return self.assertEqual(
            self.remove_csrf(first),
            self.remove_csrf(second)
        )


class HomePageTest(TestCaseWithCSRF):
    def test_home_page_returns_home_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')

        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()

        response = self.client.get('/lists/%d/' % (list_.id,))

        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertEqual(response.context['list'], correct_list)

    def test_displays_all_items(self):
        correct_list = List.objects.create()

        Item.objects.create(text='item1', list=correct_list)
        Item.objects.create(text='item2', list=correct_list)

        other_list = List.objects.create()

        Item.objects.create(text='other item1', list=other_list)
        Item.objects.create(text='other item2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')
        self.assertNotContains(response, 'other item1')
        self.assertNotContains(response, 'other item2')

    def test_can_save_a_post_request_to_an_existing_list(self):
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': 'New task item in existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'New task item in existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_post_redirects_to_list_view(self):
        correct_list = List.objects.create()

        response = self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'text': 'New task item in existing list'}
        )

        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

    def test_validation_errors_and_up_on_lists_page(self):
        list_ = List.objects.create()

        response = self.client.post(
            '/lists/%d/' % (list_.id,),
            data={'text': ''}
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')

        expected_error = escape('You can\'t have an empty list item')

        self.assertContains(response, expected_error)


class NewListTest(TestCase):
    def test_saving_a_post_request(self):
        self.client.post(
            '/lists/new',
            data={'text': 'New task item'}
        )

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'New task item')

    def test_redirects_after_post(self):
        response = self.client.post(
            '/lists/new',
            data={'text': 'New task item'}
        )

        new_list = List.objects.first()

        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={'text': ''})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

        expected_error = escape('You can\'t have an empty list item')

        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})

        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
