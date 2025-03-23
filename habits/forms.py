from django import forms

from habits.models import Habit


class CreateUpdateHabitForm(forms.ModelForm):
    
    class Meta:
        model = Habit
        fields = ['name', 'duration']
        labels = {
            'name': 'Habit',
            'duration': 'Duration',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'What new habit would you like to track?',
                }
            ),
            'duration': forms.RadioSelect(),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['duration'].required = True
        self.fields['duration'].choices = Habit.DURATION_CHOICES
        self.initial['duration'] = 60