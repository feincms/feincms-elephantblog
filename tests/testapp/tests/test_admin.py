from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from elephantblog.models import Entry

from .factories import UserFactory


class AdminTestCase(TestCase):
    def test_admin(self):
        author = UserFactory.create(is_staff=True, is_superuser=True)
        author.set_password('elephant')
        author.save()

        self.client.login(username=author.username, password='elephant')

        self.assertContains(
            self.client.get('/admin/elephantblog/entry/'),
            '0 entries',
        )

        response = self.client.post(
            '/admin/elephantblog/entry/add/',
            {
                'title': 'First entry',
                'slug': 'first-entry',
                'author': author.id,
                'language': 'en',

                'richtextcontent_set-TOTAL_FORMS': 0,
                'richtextcontent_set-INITIAL_FORMS': 0,
                'richtextcontent_set-MAX_NUM_FORMS': 1000,
            }
        )

        self.assertRedirects(
            response,
            'http://testserver/admin/elephantblog/entry/',
        )

        entry = Entry.objects.get()
        self.assertEqual(entry.published_on, None)

        response = self.client.post(
            '/admin/elephantblog/entry/{0}/'.format(entry.id),
            {
                'title': 'First entry',
                'slug': 'first-entry',
                'author': author.id,
                'language': 'en',
                'is_active': True,

                'richtextcontent_set-TOTAL_FORMS': 0,
                'richtextcontent_set-INITIAL_FORMS': 0,
                'richtextcontent_set-MAX_NUM_FORMS': 1000,
            }
        )

        entry = Entry.objects.get()
        # entry.published_on has been set automatically
        self.assertNotEqual(entry.published_on, None)
