from django.test import TestCase

from habits.forms import CreateUpdateHabitForm


class HabitViewTests(TestCase):
    
    def test_create_update_habit_form(self):

        form_data = {
           'name': 'A Test Habit', 
           'duration': 30,
        }

        form = CreateUpdateHabitForm(data=form_data, files=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['name'], 'A Test Habit')
        self.assertEqual(form.cleaned_data['duration'], 30)
        