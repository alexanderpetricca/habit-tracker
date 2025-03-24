from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

from accounts.models import SignUpCode
from habits.models import Habit


class CustomUserModelTests(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            first_name = 'Test',
            last_name = 'User',
            email = 'testuser@email.com',
            password = 'testpass123'
        )

        self.admin_user = get_user_model().objects.create_superuser(
            first_name = 'Admin',
            last_name = 'User',
            email = 'adminuser@email.com',
            password = 'testpass123'
        )

        self.habit_1 = Habit.objects.create(
            owner = self.user,
            name = 'Test Habit 1',
            duration = 7,
        )

        self.habit_1 = Habit.objects.create(
            owner = self.user,
            name = 'Test Habit 2',
            duration = 7,
        )

        self.add_customuser = Permission.objects.get(codename='add_customuser')
        self.view_customuser = Permission.objects.get(codename='view_customuser')


    def test_create_user(self):
        """
        Test user object creation.
        """        

        self.assertEqual(self.user.email, 'testuser@email.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.habit_limit, 5)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)


    def test_create_superuser(self):
        """
        Test user object superuser creation.
        """

        self.assertEqual(self.admin_user.email, 'adminuser@email.com')
        self.assertEqual(self.admin_user.first_name, 'Admin')
        self.assertEqual(self.admin_user.last_name, 'User')
        self.assertEqual(self.user.habit_limit, 5)
        self.assertTrue(self.admin_user.is_active)
        self.assertTrue(self.admin_user.is_staff)
        self.assertTrue(self.admin_user.is_superuser)

    
    def test_string_representation(self):
        """
        Test user model string method.
        """

        self.assertEqual(str(self.user), self.user.email)
        self.assertEqual(str(self.admin_user), self.admin_user.email)


    def max_habits_created(self):
        """
        Tests the max habits created method.
        """

        self.assertTrue(self.user.max_habits_created())
        
        # Reduce habit_limit from 5, to 2, and test again to ensure False.
        self.user.habit_limit = 2
        self.user.save()
        self.user.refresh_from_db()
        self.assertFalse(self.user.max_habits_created())



class SignupCodeModelTests(TestCase):

    def setUp(self):
        self.signup_code = SignUpCode.objects.create()


    def test_create_signupcode(self):
        self.assertIsNotNone(self.signup_code.id)
        self.assertIsNotNone(self.signup_code.created)
        self.assertTrue(len(self.signup_code.code) == 12)


    def test_signupcode_string_method(self):
        self.assertEqual(str(self.signup_code), self.signup_code.code)
        