from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AccountFlowTests(TestCase):
    def test_login_accepts_registered_email(self):
        User.objects.create_user(
            username='emailmember',
            email='asdf@sina.com',
            password='SafePassword!482',
        )

        response = self.client.post(
            reverse('login_user'),
            {'username': 'asdf@sina.com', 'password': 'SafePassword!482'},
        )

        self.assertRedirects(response, reverse('dashboard'))
        self.assertContains(self.client.get(reverse('dashboard')), 'emailmember')

    def test_registration_login_dashboard_and_logout_flow(self):
        registration_response = self.client.post(
            reverse('register_user'),
            {
                'username': 'newmember',
                'email': 'newmember@example.com',
                'password1': 'SafePassword!482',
                'password2': 'SafePassword!482',
            },
        )

        self.assertRedirects(registration_response, reverse('login_user'))
        self.assertTrue(User.objects.filter(username='newmember').exists())

        login_response = self.client.post(
            reverse('login_user'),
            {'username': 'newmember', 'password': 'SafePassword!482'},
        )
        self.assertRedirects(login_response, reverse('dashboard'))

        home_response = self.client.get(reverse('home'))
        self.assertEqual(home_response.status_code, 200)
        self.assertContains(home_response, 'Log In')

        dashboard_response = self.client.get(reverse('dashboard'))
        self.assertContains(dashboard_response, 'newmember')
        self.assertContains(dashboard_response, 'newmember@example.com')

        self.client.get(reverse('logout_user'))
        self.assertRedirects(
            self.client.get(reverse('dashboard')),
            f"{reverse('login_user')}?next={reverse('dashboard')}",
        )
