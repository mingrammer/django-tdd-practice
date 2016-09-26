import re

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item
from lists.views import home_page


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

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()

        response = home_page(request)

        expected_html = render_to_string('home.html', request=request)

        self.assertEqualExceptCSRF(response.content.decode(), expected_html)


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'First item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Second item'
        second_item.save()

        saved_items = Item.objects.all()

        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'First item')
        self.assertEqual(second_saved_item.text, 'Second item')


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        Item.objects.create(text='item1')
        Item.objects.create(text='item2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')


class NewListTest(TestCase):

    def test_saving_a_post_request(self):
        self.client.post(
            '/lists/new',
            data={'item_text': 'New task item'}
        )

        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'New task item')

    def test_redirects_after_post(self):
        response = self.client.post(
            '/lists/new',
            data={'item_text': 'New task item'}
        )

        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')

