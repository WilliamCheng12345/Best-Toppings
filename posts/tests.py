from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post, Comment


# Create your tests here.
class PostsTests(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='testUser',
            email='test@email.com',
            password='testPassword'
        )

        self.user2 = get_user_model().objects.create_user(
            username='secondTestUser',
            email='secondTest@email.com',
            password='secondTestPassword'
        )

        self.post = Post.objects.create(
            title='Test title',
            author=self.user1,
            meat='chicken, bacon',
            non_meat='pineapple',
            body='Test body'
        )

        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user1,
            comment='Test comment'
        )

    def test_posts_list_view(self):
        response = self.client.get(reverse('posts_list'))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'posts_list.html')

        self.assertContains(response, 'Test title')
        self.assertContains(response, 'chicken, bacon')
        self.assertContains(response, 'pineapple')
        self.assertContains(response, 'Test body')

    def test_posts_detail_view(self):
        response = self.client.get('/1/')
        no_response = self.client.get('/1000/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)

        self.assertTemplateUsed(response, 'posts_detail.html')

        self.assertContains(response, 'Test title')
        self.assertContains(response, 'chicken, bacon')
        self.assertContains(response, 'pineapple')
        self.assertContains(response, 'Test body')

    def test_posts_create_view(self):
        self.client.login(
            username='testUser',
            password='testPassword'
        )

        response = self.client.post(reverse('posts_new'), {
            'title': 'Second test title',
            'meat': 'chicken, bacon, ham, beef',
            'non_meat': 'pineapple, black olives',
            'body': 'Second test body'
        }, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Second test title')
        self.assertContains(response, 'chicken, bacon, ham, beef')
        self.assertContains(response, 'pineapple, black olives')
        self.assertContains(response, 'Second test body')

    def test_posts_update_view(self):
        self.client.login(
            username='testUser',
            password='testPassword'
        )

        response = self.client.post(reverse('posts_edit', kwargs={'pk': '1'}), {
            'title': 'Third test title',
            'meat': 'chicken, bacon, ham, pepperoni, beef',
            'non_meat': 'pineapple, black olives, green peppers',
            'body': 'Third test body'
        }, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Third test title')
        self.assertContains(response, 'chicken, bacon, ham, pepperoni, beef')
        self.assertContains(response, 'pineapple, black olives, green peppers')
        self.assertContains(response, 'Third test body')

    def test_posts_delete_view(self):
        self.client.login(
            username='testUser',
            password='testPassword'
        )

        response = self.client.post(reverse('posts_delete', kwargs={'pk': '1'}), follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, 'Test title')
        self.assertNotContains(response, 'chicken, bacon')
        self.assertNotContains(response, 'pineapple')
        self.assertNotContains(response, 'Test body')

    def test_user_delete_only_their_posts(self):
        self.client.login(
            username='secondTestUser',
            password='secondTestPassword',
        )

        response = self.client.get(reverse('posts_delete', kwargs={'pk': '1'}))

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_user_edit_only_their_posts(self):
        self.client.login(
            username='secondTestUser',
            password='secondTestPassword',
        )

        response = self.client.post(reverse('posts_edit', kwargs={'pk': '1'}), {
            'title': 'Third test title',
            'meat': 'chicken, bacon, ham, pepperoni, beef',
            'non_meat': 'pineapple, black olives, green peppers',
            'body': 'Third test body'
        })

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_comments_create_view(self):
        self.client.login(
            username='testUser',
            password='testPassword',
        )

        response = self.client.post(reverse('comments_new', kwargs={'pk': '1'}), {
            'comment': 'This is the second test comment',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is the second test comment')

    def test_comments_update_view(self):
        self.client.login(
            username='testUser',
            password='testPassword',
        )

        response = self.client.post(reverse('comments_edit', kwargs={'pk': '1', 'postpk': '1'}), {
            'comment': 'This is the third comment.',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is the third comment.')

    def test_comments_delete_view(self):
        self.client.login(
            username='testUser',
            password='testPassword',
        )

        response = self.client.post(reverse('comments_delete', kwargs={'pk': '1', 'postpk': '1'}), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test comment')

    def test_user_edit_only_their_comments(self):
        self.client.login(
            username='secondTestUser',
            password='secondTestPassword',
        )

        response = self.client.get(reverse('posts_edit', kwargs={'pk': '1'}), {
            'comment': 'This is the third comment'
        })

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_user_delete_only_their_comments(self):
        self.client.login(
            username='secondTestUser',
            password='secondTestPassword',
        )

        response = self.client.get(reverse('comments_delete', kwargs={'pk': '1', 'postpk': '1'}))

        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_logged_in_user_posts_only(self):
        response = self.client.post(reverse('posts_new'), {
            'title': 'Second test title',
            'meat': 'chicken, bacon, ham, beef',
            'non_meat': 'pineapple, black olives',
            'body': 'Second test body'
        }, follow=True)

        self.assertTemplateUsed(response, 'registration/login.html')

    def test_logged_in_user_comments_only(self):
        response = self.client.post(reverse('posts_new'), {
            'comment': 'This is second comment'
        }, follow=True)

        self.assertTemplateUsed(response, 'registration/login.html')
