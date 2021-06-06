from django.db import models
from django.contrib.auth.models import User

# Create your models here.
GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "female"),
    ("other", "other"),
    
)


class Catagory(models.Model):
    catagory_name= models.CharField(max_length=250 )
    def __str__(self):
        return self.catagory_name

class StudentUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField( max_length=50 , null=True)
    image = models.FileField(null=True)
    gender = models.CharField(null=True , choices=GENDER_CHOICES, max_length=50)
    type = models.CharField(max_length=50 , null=True )
    def __str__(self):
        return self.user.username


class RecruiterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='null')

class AcceptedRecruiterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='Accepted')

class rejectRecruiterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='Rejected')




class Recruiter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField( max_length=50 , null=True)
    image = models.FileField(null=True)
    gender = models.CharField(null=True , choices=GENDER_CHOICES, max_length=50)
    company = models.CharField(max_length=100 , null=True)
    status =models.CharField(max_length=20 , null=True)
    type = models.CharField(max_length=50 , null=True )
    objects = models.Manager()
    pendingrec = RecruiterManager()
    acceptcompany = AcceptedRecruiterManager()
    rejcomp = rejectRecruiterManager()
    def __str__(self):
        return self.company

    class Meta:
        verbose_name ="Company"
        verbose_name_plural = "Company"


class Add_job(models.Model):
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    title = models.CharField(max_length=30, null=True)
    position = models.CharField(max_length=30, null=True)
    image = models.FileField(null=True)
    description = models.CharField(max_length=500, null=True)
    experience = models.CharField(max_length=30, null=True)
    catagory = models.ForeignKey(Catagory,on_delete=models.CASCADE )
    location = models.CharField(max_length=30, null=True)
    skills = models.CharField(max_length=30, null=True)
    salary=models.CharField(max_length=30, null=True)
    timee = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.title + " " + self.recruiter.company


class Apply(models.Model):
    job = models.ForeignKey(Add_job, on_delete=models.CASCADE, null=True)
    sign = models.ForeignKey(StudentUser, on_delete=models.CASCADE, null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.sign.user.username + " " + self.job.title


class allusers(models.Model):
    email=models.EmailField()
    def __str__(self):
        return self.email
