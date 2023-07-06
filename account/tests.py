# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.contrib.auth import authenticate, get_user_model
from django.db.utils import IntegrityError
from django.urls import reverse

User = get_user_model()


class A(TestCase):
    def test_auth001(self):
        user = authenticate(uid='a001001')
        self.assertIsInstance(user, User)

        user = authenticate(uid='a001001')
        self.assertIsInstance(user, User)

        user = authenticate(uid='b002002')
        self.assertIsInstance(user, User)

    def test_auth002(self):
        with self.assertRaises(Exception) as e:
            user = authenticate(uid='b001001')
            print(user)
        self.assertIsInstance(e.exception, Exception)

    def test_create_user_001(self):
        user = User.objects.create_user(
            uid='q2917013',
            division='フリーター',
            first_name='よこた',
            last_name='よしのり',
            email='yokota@example.jp',
            is_staff=True,
            is_active=True,
            password='pswd0000',
        )
        self.assertIsInstance(user, User)

    def test_create_user_002(self):
        uid = 'q2917013'
        u0 = User.objects.create_user(uid=uid)
        self.assertIsInstance(u0, User)
        with self.assertRaises(Exception) as e:
            u1 = User.objects.create_user(uid=uid)
            self.assertIsInstance(u1, User)
        self.assertIsInstance(e.exception, IntegrityError)

    def test_create_superuser_001(self):
        user = User.objects.create_superuser(
            uid='q2917013',
            division='フリーター',
            first_name='よこた',
            last_name='よしのり',
            email='yokota@example.jp',
            is_staff=True,
            is_active=True,
            password='pswd0000',
        )
        self.assertIsInstance(user, User)

    def test_create_superuser_002(self):
        uid = 'q2917013'
        u0 = User.objects.create_superuser(uid=uid)
        self.assertIsInstance(u0, User)
        with self.assertRaises(Exception) as e:
            u1 = User.objects.create_superuser(uid=uid)
            self.assertIsInstance(u1, User)
        self.assertIsInstance(e.exception, IntegrityError)


class B(TestCase):
    def setUp(self):
        self.client = Client()

    def test_A(self):
        r = self.client.get(reverse('account:login'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'autofocus')
        self.assertContains(r, 'required')
        self.assertIn('form', r.context)
        # print(r.content)

    def test_login(self):
        r = self.client.post(reverse('account:login'), {'uid': 'a001001'})
        self.assertRedirects(r, reverse('main:top'))

    def test_login_error(self):
        r = self.client.post(reverse('account:login'), {'uid': 'a001011'})
        self.assertIsNotNone(r.context)
        self.assertIn('form', r.context)
        e = r.context['form'].errors.get('uid', '')
        self.assertTrue(e)
        for x in list(e):
            self.assertIn('No such user:', x)

    def test_logout(self):
        r = self.client.get(reverse('account:logout'))
        self.assertRedirects(r, reverse('main:top'))
