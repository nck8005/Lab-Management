from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    admission_no = models.CharField(max_length=10)

    def __str__(self):
        return self.username


class CodeSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    code = models.TextField()
    output = models.TextField(blank=True, null=True)  
    pdf_generated = models.BooleanField(default=False)  # Tracks whether PDF is generated for this submission
    

    def __str__(self):
        return f"{self.user.username} - {self.question[:50]}"
