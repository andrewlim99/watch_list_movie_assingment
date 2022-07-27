from rest_framework import serializers
from playground.models import WatchList


class WatchListSerializer(serializers.ModelSerializer):
	class Meta:
		model = WatchList
		fields = '__all__'
