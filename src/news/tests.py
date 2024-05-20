from django.test import TestCase
from django.utils import timezone
from .models import newsBit

class newsTests(TestCase):
    def setUp(self):
        self.newsBit = newsBit.objects.create(
            title = "Politics with Elmo",
            channel= "PBS",
            transcript = "THIS WILL BE REALLY LONG I THINK IT HAS OT BE LONG IM NOT SURE THIS IS A TEST",
            category= "Politics",
            publication_date = timezone.now(),
            video_url = "https://www.youtube.com/watch?v=mH7XhHEb-ck",
            image = "https://img.youtube.com/vi/mH7XhHEb-ck/hqdefault.jpg",
            guid = "de194720-7b4c-49e2-a05f-432436d3fetr",
        )

    def test_newsBit_content(self):
        self.assertEqual(self.newsBit.title, "Politics with Elmo")
        self.assertEqual(self.newsBit.video_url, "https://www.youtube.com/watch?v=mH7XhHEb-ck")
        self.assertEqual(
            self.newsBit.guid, "de194720-7b4c-49e2-a05f-432436d3fetr"
        )

    def test_newsBit_str_representation(self):
        self.assertEqual(
            str(self.newsBit), "Politics: Politics with Elmo: PBS"
        )