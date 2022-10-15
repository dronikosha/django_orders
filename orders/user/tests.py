from urllib import response
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import TestCase
from main.models import Order


class OrderViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
            email= '123@123.ru'
        )
        self.user.save()
        
    def test_create_order(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/create/', {'title': 'test', 'text': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().title, 'test')
        
    def test_create_order_no_title(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/create/', {'title': '', 'text': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)
        
    def test_create_order_no_text(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/create/', {'title': 'test', 'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)
        
    def test_create_order_no_title_no_text(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/create/', {'title': '', 'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 0)
        
    def test_create_order_not_logged_in(self):
        response = self.client.post('/create/', {'title': 'test', 'text': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)
        
    def test_update_order(self):
        self.client.login(username='testuser', password='12345')
        self.client.post('/create/', {'title': 'test', 'text': 'test'})
        response = self.client.post('/update/1', {'title': 'test2', 'text': 'test2'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().title, 'test2')
        
    def test_update_order_no_title(self):
        self.client.login(username='testuser', password='12345')
        self.client.post('/create/', {'title': 'test', 'text': 'test'})
        response = self.client.post('/update/1', {'title': '', 'text': 'test2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().title, 'test')
    
    def test_update_order_no_text(self):
        self.client.login(username='testuser', password='12345')
        self.client.post('/create/', {'title': 'test', 'text': 'test'})
        response = self.client.post('/update/1', {'title': 'test2', 'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().title, 'test')
        
    def test_patch_order(self):
        self.client.login(username='testuser', password='12345')
        self.client.post('/create/', {'title': 'test', 'text': 'test'})
        response = self.client.patch('/update/1', {'title': 'test2'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().title, 'test')
        
    def test_delete_order(self):
        self.client.login(username='testuser', password='12345')
        self.client.post('/create/', {'title': 'test', 'text': 'test'})
        response = self.client.post('/delete/1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)
        
    def test_delete_not_logged_in(self):
        self.client.post('/create/', {'title': 'test', 'text': 'test'})
        response = self.client.post('/delete/1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)
        
    def test_delete_not_owner(self):
        self.client.force_login(User.objects.get_or_create(username='testuser2')[0])
        self.client.post('/create/', {'title': 'test', 'text': 'test'})
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/delete/1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        
    def test_delete_not_exists(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/delete/1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)
        
    def test_delete_not_owner_not_exists(self):
        self.client.force_login(User.objects.get_or_create(username='testuser2')[0])
        self.client.post('/create/', {'title': 'test', 'text': 'test'})
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/delete/2')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        
    def test_delete_not_logged_in_not_exists(self):
        self.client.post('/create/', {'title': 'test', 'text': 'test'})
        response = self.client.post('/delete/2')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)
        
    def test_delete_not_logged_in_not_owner(self):
        self.client.force_login(User.objects.get_or_create(username='testuser2')[0])
        self.client.post('/create/', {'title': 'test', 'text': 'test'})
        response = self.client.post('/delete/1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)
        
    def test_update_not_owner(self):
        self.client.force_login(User.objects.get_or_create(username='testuser2')[0])
        self.client.post('/create/', {'title': 'test', 'text': 'test'})
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/update/1', {'title': 'test2', 'text': 'test2'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().title, 'test')
        
    def test_update_not_exists(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post('/update/1', {'title': 'test2', 'text': 'test2'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 0)
