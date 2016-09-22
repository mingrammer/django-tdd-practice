import re

from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

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

    def test_home_page_can_save_a_post_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'New task item'

        response = home_page(request)

        self.assertIn('New task item', response.content.decode())

        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'New task item'},
            request=request
        )

        self.assertEqualExceptCSRF(response.content.decode(), expected_html)
