from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from habits.models import Habit, CompletedDay


class HabitViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            first_name = 'Test',
            last_name = 'User',
            email = 'test.user@email.com',
            password = 'TestPass123',
        )
        
        self.habit = Habit.objects.create(
            owner = self.user,
            name = 'A Test Habit',
            duration = 7,
        )


    # Home
    def test_home_view_user_logged_out(self):
        """
        Test user is redirected to login after attempting to access homepage, 
        without being logged in.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('account_login')}?next=/")

        response = self.client.get(f"{reverse('account_login')}?next=/")
        self.assertTemplateUsed(response, 'account/login.html')
        self.assertContains(response, 'Login')


    def test_home_view_user_logged_in_no_habit(self):
        """
        Test user is redirected to create habit page, after attempting to 
        access homepage, when logged in, but when they have no active habits.
        """

        # Soft delete habit, so user has no active habits for this test.
        self.habit.soft_delete()
        
        self.client.login(email="test.user@email.com", password="TestPass123")
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('habits/create-habit.html')


    def test_home_view_user_logged_in_with_habit(self):
        """
        Test home page is rendered, when user is logged in, and they have an 
        active habit.
        """
        
        self.client.login(email="test.user@email.com", password="TestPass123")
        
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habits/habit.html')
        self.assertContains(response, 'A Test Habit')


    # Habit
    def test_habit_view_user_logged_out(self):
        """
        Test user is redirected to login after attempting to access habit page, 
        without being logged in.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('habit', kwargs={'pk': self.habit.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('account_login')}?next=/habit/{self.habit.pk}/")

        response = self.client.get(f"{reverse('account_login')}?next=/habit/{self.habit.pk}/")
        self.assertTemplateUsed(response, 'account/login.html')
        self.assertContains(response, 'Login')   


    def test_habit_view_user_logged_in(self):
        """
        Test habit page is rendered, when user is logged in.
        """
        
        self.client.login(email="test.user@email.com", password="TestPass123")
        
        response = self.client.get(reverse('habit', kwargs={'pk': self.habit.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habits/habit.html')
        self.assertContains(response, 'A Test Habit')
    
    
    # Create Habit
    def test_create_habit_view_user_logged_out(self):
        """
        Test user is redirected to login after attempting to access create 
        habit page, without being logged in.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('create_habit'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('account_login')}?next=/create-habit/")

        response = self.client.get(f"{reverse('account_login')}?next=/create-habit/")
        self.assertTemplateUsed(response, 'account/login.html')
        self.assertContains(response, 'Login') 


    def test_create_habit_view_user_logged_in_get(self):
        """
        Test create habit page is rendered on GET to create habit view, when 
        user is logged in.
        """
        
        self.client.login(email="test.user@email.com", password="TestPass123")
        
        response = self.client.get(reverse('create_habit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habits/create-habit.html')
        self.assertContains(response, 'New Habit')


    def test_create_habit_view_user_logged_in_post(self):
        """
        Tests new habit is created on POST to create habit view when user is 
        logged in, and that the user is redirected afterward.
        """
        
        self.client.login(email="test.user@email.com", password="TestPass123")
        
        form_data = {
           'name': 'Another Test Habit', 
           'duration': 30,
        }

        response = self.client.post(reverse('create_habit'), data=form_data)
        self.assertEqual(response.status_code, 302)

        try:
            Habit.objects.get(name='Another Test Habit')
        except ObjectDoesNotExist:
            self.fail('New habit could not be found.')


    # Max Habits Created
    def test_create_habit_view_user_logged_out(self):
        """
        Test user is redirected to login after attempting to access max habits 
        reached page, without being logged in.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('max_habits_created'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('account_login')}?next=/max-habits-created/")

        response = self.client.get(f"{reverse('account_login')}?next=/max-habits-created/")
        self.assertTemplateUsed(response, 'account/login.html')
        self.assertContains(response, 'Login')


    # Completed Day Toggle
    def test_toggle_completed_day_view_user_logged_out(self):
        """
        Test user is redirected to login after attempting to access the toggle 
        completed day view, without being logged in.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('habit_completed_day_toggle', kwargs={'pk': self.habit.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('account_login')}?next=/habit-day-toggle/{self.habit.pk}/")

        response = self.client.get(f"{reverse('account_login')}?next=/habit-day-toggle/{self.habit.pk}/")
        self.assertTemplateUsed(response, 'account/login.html')
        self.assertContains(response, 'Login')


    def test_toggle_completed_day_view_user_logged_in_get(self):
        """
        Test 405 is returned when user is logged in and sends a GET request to 
        the toggle completed day view.
        """
        
        self.client.login(email="test.user@email.com", password="TestPass123")
        
        response = self.client.get(reverse('habit_completed_day_toggle', kwargs={'pk': self.habit.pk}))
        self.assertEqual(response.status_code, 405)


    def test_toggle_completed_day_view_user_logged_in_post(self):
        """
        Test toggle completed day view creates new completed day object on 
        POST, and if a completed day object for the specified habit already 
        exists for the current day, deletes it.
        """
        
        self.client.login(email="test.user@email.com", password="TestPass123")
        
        # Create CompletedDay object on first request
        response = self.client.post(reverse('habit_completed_day_toggle', kwargs={'pk': self.habit.pk}))
        self.assertEqual(response.status_code, 200)

        try:
            new_completed_day = CompletedDay.objects.get(
                habit__id=self.habit.id, 
                day=str(timezone.now().date()),
            )
        except ObjectDoesNotExist:
            self.fail('Could not find completed day object.')


        # Delete CompletedDay object if already exists
        response = self.client.post(reverse('habit_completed_day_toggle', kwargs={'pk': self.habit.pk}))
        self.assertEqual(response.status_code, 200)

        try:
            CompletedDay.objects.get(
                habit__id=self.habit.id, 
                day=str(timezone.now().date()),
            )
            self.fail('Completed day object was not deleted.')  
        except ObjectDoesNotExist:
            pass


    # Delete Habit
    def test_delete_habit_view_user_logged_out(self):
        """
        Test user is redirected to login after attempting to delete habit 
        page, without being logged in.
        """
        
        self.client.logout()
        
        response = self.client.get(reverse('delete_habit', kwargs={'pk': self.habit.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('account_login')}?next=/delete-habit/{self.habit.pk}/")

        response = self.client.get(f"{reverse('account_login')}?next=/delete-habit/{self.habit.pk}/")
        self.assertTemplateUsed(response, 'account/login.html')
        self.assertContains(response, 'Login')


    def test_delete_habit_view_user_logged_in_get(self):
        """
        Test delete habit page is rendered on GET to delete habit view, when 
        user is logged in.
        """
        
        self.client.login(email="test.user@email.com", password="TestPass123")
        
        response = self.client.get(reverse('delete_habit', kwargs={'pk': self.habit.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'habits/delete-habit.html')
        self.assertContains(response, 'Delete Habit')


    def test_delete_habit_view_user_logged_in_post(self):
        """
        Tests habit is deleted on POST to delete habit view, when user is 
        logged in, and that the user is redirected afterward.
        """        
        
        self.client.login(email="test.user@email.com", password="TestPass123")
        
        response = self.client.post(reverse('delete_habit', kwargs={'pk': self.habit.pk}))
        self.assertEqual(response.status_code, 302)

        try:
            Habit.objects.get(
                name = 'A Test Habit',
                deleted = False,
            )
            self.fail('Habit object was not deleted.')  
        except ObjectDoesNotExist:
            pass