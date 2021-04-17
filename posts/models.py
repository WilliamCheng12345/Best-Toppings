from django.db import models
from multiselectfield import MultiSelectField
from django.urls import reverse


# Create your models here.
class Post(models.Model):
    MEATS = (
        ("no meat", "no meat"),
        ("chicken", "chicken"),
        ("bacon", "bacon"),
        ("sausage", "sausage"),
        ("ham", "ham"),
        ("pepperoni", "pepperoni"),
        ("beef", "beef"),
    )

    NON_MEATS = (
        ("no nonmeat", "no nonmeat"),
        ("pineapple", "pineapple"),
        ("black olives", "black olives"),
        ("mushrooms", "mushrooms"),
        ("onion", "onion"),
        ("green peppers", "green peppers"),
        ("banana peppers", "banana peppers"),
        ("spinach", "spinach"),
    )

    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    meat = MultiSelectField(
        choices=MEATS,
        default='1',
    )
    non_meat = MultiSelectField(
        choices=NON_MEATS,
        default='1',
    )
    body = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts_detail', args=[self.pk])


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    comment = models.CharField(max_length=300)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse('posts_detail', args=[self.post.pk])
