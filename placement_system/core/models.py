from django.db import models
from django.contrib.auth.models import User
# Create your models here.

BRANCH_CHOICES = [
    ('CSE', 'CSE'),
    ('IT', 'IT'),
    ('ECE', 'ECE'),
    ('MECH', 'MECH'),
    ('CIVIL', 'CIVIL'),
]

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    branch = models.CharField(max_length=100,choices=BRANCH_CHOICES)
    tenth_percentage = models.FloatField()
    tweleve_percentage = models.FloatField()
    cgpa = models.FloatField()
    resume = models.FileField(upload_to='resumes/',null=True,blank=True)

    def __str__(self):
        return self.user.username

#Company model
class Company(models.Model):
    
    company_name = models.CharField(max_length=200)
    job_role = models.CharField(max_length=200)
    ctc = models.FloatField() 
    drive_date = models.DateField(null=True,blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    eligibility_cgpa = models.FloatField() 
    allowed_branches = models.CharField(
        max_length=20,
        choices=BRANCH_CHOICES,
        default='CSE'
    )
    drive_notice = models.FileField(upload_to='drive_notices/', null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='company_logos/', null=True, blank=True) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def  __str__(self):
        return self.company_name


# Application model

class application(models.Model):
    STATUS_CHOICES = (
        ('Applied','Applied'),
        ('Selected','Selected'),
        ('Rejected','Rejected'),
    )
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Applied')

     # ✅ NEW FIELDS
    interview_date = models.DateField(null=True, blank=True)
    interview_time = models.TimeField(null=True, blank=True)
    interview_mode = models.CharField(max_length=20, blank=True)  # Online / Offline
    interview_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.company.company_name}"
    

class MockTest(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # Aptitude / Technical / HR

    def __str__(self):
        return f"{self.company.company_name} - {self.title}"


class Question(models.Model):
    mock_test = models.ForeignKey(MockTest, on_delete=models.CASCADE)
    question_text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text[:50]


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=200)