from django import forms

class RatingQuestionsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')

        super().__init__(*args, **kwargs)
        for i, question in enumerate(questions):
            self.fields[f'question_{i+1}'] = forms.ChoiceField(choices=question['options'], label=question['text'])