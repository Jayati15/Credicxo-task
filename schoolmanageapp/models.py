from django.db import models
from django.contrib.auth.models import User

# Create your models here.
ACCOUNT_TYPE = (('1','Superadmin'),
                ('2','teacher'),
                ('3','Student'))

class UserAccount(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	account_type = models.CharField(max_length=10,choices=ACCOUNT_TYPE)
	def __str__(self):
		return self.user.username



class forget_otp(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    otp = models.CharField(max_length=10)
    expire  = models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
    attempt = models.IntegerField(default=0)
    is_used = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

# Create your models here.
