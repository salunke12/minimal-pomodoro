from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PomodoroSession(models.Model):
    TYPE_CHOICES = [
        ('WORK', 'Work Session'),
        ('SHORT_BREAK', 'Short Break'),
        ('LONG_BREAK', 'Long Break'),
    ]
    
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    task_label = models.CharField(max_length=100, default="General Focus")
    session_type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='WORK')
    duration_minutes = models.IntegerField(default=25)
    completed_at = models.DateTimeField(auto_now_add=True)
    completed_successfully = models.BooleanField(default=True)
    tree_type = models.CharField(max_length=20, default='OAK')

    def __str__(self):
        status = "Completed" if self.completed_successfully else "Interrupted"
        return f"{self.task_label} ({self.get_session_type_display()}) - {status} at {self.completed_at.strftime('%b %d, %H:%M')}"
