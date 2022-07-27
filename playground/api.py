from rest_framework.response import Response
from rest_framework.decorators import api_view
from playground.models import WatchList
from .serializers import WatchListSerializer


@api_view(['POST'])
def insert_movie_to_user_watch_list(request):
    serializer = WatchListSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    else:
        return Response(serializer.errors)

    return Response(serializer.data)
