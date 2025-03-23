from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from habits.models import Habit, CompletedDay


class HabitModelTests(TestCase):
    
    def setUp(self):
        
        self.today_str = str(timezone.now().date())
        
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

        self.completed_day = CompletedDay.objects.create(
            habit = self.habit,
        )        


    def test_habit_model_creation(self):
        self.assertIsNotNone(self.habit.id)
        self.assertIsNotNone(self.habit.created_at)
        self.assertEqual(self.habit.owner.id, self.user.id)
        self.assertEqual(self.habit.name, 'A Test Habit')
        self.assertEqual(self.habit.duration, 7)


    def test_habit_string_method(self):
        self.assertEqual(str(self.habit), 'A Test Habit')


    def test_habit_generate_grid_method(self):
        grid = self.habit.generate_grid()
        first_element = grid.get(list(grid.keys())[0])

        self.assertEqual(type(grid), dict)
        self.assertEqual(len(grid), 7)
        self.assertEqual(len(first_element), 4)
        self.assertEqual(
            tuple(first_element.keys()), 
            ('date', 'completed', 'is_past', 'is_today')
        )
        self.assertEqual(first_element.get('date'), self.today_str)
        self.assertFalse(first_element.get('is_past'))
        self.assertTrue(first_element.get('completed'))
        self.assertTrue(first_element.get('is_today'))


    def test_habit_soft_delete(self):
        self.habit.soft_delete()
        
        try:
            deleted_habit = Habit.objects.get(name='A Test Habit', deleted=True)
            self.assertTrue(deleted_habit.deleted)
            self.assertIsNotNone(deleted_habit.deleted_at)
        except ObjectDoesNotExist:
            self.fail('Cannot find deleted habit.')


    def test_completed_day_model_creation(self):
        self.assertIsNotNone(self.completed_day.id)
        self.assertEqual(self.completed_day.habit.id, self.habit.id)
        self.assertIsNotNone(self.completed_day.day)


    def test_completed_day_string_method(self):
        self.assertEqual(str(self.completed_day), self.today_str)