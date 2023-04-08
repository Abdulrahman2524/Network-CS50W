from django.test import TestCase
from .models import *
from datetime import datetime
# Create your tests here.

class PostTestCase(TestCase):
    def setUp(self):
        # create post.
        a1 = newPost.objects.create(text="Good Night!", date=datetime.now())
        a2 = newPost.objects.create(text="Good Bye!", date=datetime.now())

    # test.
    def test_post(self):
        a = newPost.objects.all()
        self.assertEqual(a.count(), 2)
