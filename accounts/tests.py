from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from posts.models import Post


# Create your tests here.
class AccountsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testUser',
            email='test@email.com',
            password='testPassword'
        )

        self.post = Post.objects.create(
            title='Test title',
            author=self.user,
            meat='chicken, bacon',
            non_meat='pineapple',
            body='Test body'
        )

    def test_account_view(self):
        self.client.login(
            username='testUser',
            password='testPassword'
        )

        response = self.client.get(reverse('account'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'account.html')

        self.assertContains(response, 'Test title')
        self.assertContains(response, 'chicken, bacon')
        self.assertContains(response, 'pineapple')
        self.assertContains(response, 'Test body')

    def test__logged_in_account_only(self):
        response = self.client.get(reverse('account'), follow=True)

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')
