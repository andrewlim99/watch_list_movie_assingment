from django.db import models


# Create your models here.
class RegisterUser(models.Model):
	username = models.CharField(max_length=50)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	password = models.CharField(max_length=50)

	class Meta:
		db_table = "user"
