from django import forms

class QuizForm(forms.Form):
    def __init__(self, data, question, *args, **kwargs):
        self.question = question
        choices = []
        for answer in question.answers.all():
            choices.append((answer.pk, answer.answer, ))
        self.field = forms.ChoiceField(label=question.question, choices=choices)
        super(QuizForm, self).__init__(data, *args, **kwargs)
