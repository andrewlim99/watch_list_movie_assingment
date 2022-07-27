from django.db import models


# Create your models here.
class User(models.Model):
	user_name = models.CharField(max_length=50)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	date_joined = models.DateField()

	class Meta:
		db_table = "user"


class WatchList(models.Model):
	user_id = models.IntegerField(blank=True)
	user_name = models.CharField(max_length=50, blank=True)
	movie_id = models.CharField(max_length=50, blank=True)
	movie_title = models.CharField(max_length=50, blank=True)
	movie_notes = models.CharField(max_length=500, blank=True)
	movie_url = models.CharField(max_length=100, blank=True)
	date_added = models.DateField(auto_now_add=True)

	class Meta:
		db_table = "watch_list"


class UserActivity(models.Model):
	user_id = models.IntegerField()
	activity = models.CharField(max_length=50)
	activity_date = models.DateField()

	class Meta:
		db_table = "user_activity"
