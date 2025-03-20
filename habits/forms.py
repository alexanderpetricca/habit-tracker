from django import forms

from habits.models import Habit


class CreateUpdateHabitForm(forms.ModelForm):
    
    class Meta:
        model = Habit
        fields = ['name',]
        labels = {
            'name': 'Habit'
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'What new habit would you like to track?',
                    'class': 'w-full my-5 p-4 text-white bg-zinc-800'
                }
            )
        }