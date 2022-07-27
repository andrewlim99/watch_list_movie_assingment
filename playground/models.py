from django.db import models


# Create your models here.
class WatchList(models.Model):
	user_id = models.IntegerField()
	user_name = models.CharField(max_length=50)
	movie_id = models.CharField(max_length=50)
	movie_title = models.CharField(max_length=50)
	movie_notes = models.CharField(max_length=500, blank=True)
	movie_url = models.CharField(max_length=100)

	class Meta:
		db_table = "watch_list"
