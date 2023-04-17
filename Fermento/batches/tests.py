from django.test import TestCase


from .models import QrCode, Batch
from recipe_manager.models import recipe
from django.contrib.auth.models import User

class QrCodeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser1', password='12345')
        self.recipe1 = recipe.objects.create(name="kombucha", owner=self.user)
        self.batch1 = Batch.objects.create(name="batch1", owner=self.user,related_recipe=self.recipe1)
        self.qr1 = QrCode.objects.create(name="qrcode1", owner=self.user, batch=self.batch1)
        self.qr2 = QrCode.objects.create(name="qrcode2", owner=self.user)

    def test_get_qrcode_for_batch(self):
        self.assertEqual(self.batch1.get_qrcode(), self.qr1)