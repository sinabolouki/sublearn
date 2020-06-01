from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    name = models.CharField(max_length=200)
    creation = models.DateTimeField(auto_now_add=True)
    time_minutes = models.IntegerField(default=15)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(Quiz, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        if created:
            #TODO, write questions
            pass
        return obj


class Question(models.Model):
    question = models.CharField(max_length=1000)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    values = models.IntegerField(default=1)

    def __unicode__(self):
        return self.question


class Answer(models.Model):
    answer = models.CharField(max_length=300)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    pos = models.IntegerField()
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ('pos', )


class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    ended = models.BooleanField(default=False)


class QuestionAttempt(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.ForeignKey(Answer, on_delete=models.CASCADE)

