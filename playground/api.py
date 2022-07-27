from rest_framework.response import Response
from rest_framework.decorators import api_view
from playground.models import WatchList
from .serializers import WatchListSerializer
from rest_framework import status


@api_view(['POST'])
def insert_movie_to_user_watch_list(request):
    serializer = WatchListSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    else:
        return Response({"message": "Failed to insert data"}, status=status.HTTP_417_EXPECTATION_FAILED)

    return Response(serializer.data)


@api_view(['GET'])
def get_user_watch_list(request):
    user_id = request.query_params["user_id"]
    watch_list = WatchList.objects.filter(user_id=user_id).values()
    serializer = WatchListSerializer(watch_list, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def delete_watch_list(request, pk):
    watch_list = WatchList.objects.get(pk=pk)
    watch_list.delete()
    return Response({"message": "Successfully Delete"})


@api_view(['PUT'])
def update_movie_notes(request, pk):
    watch_list = WatchList.objects.get(pk=pk)
    serializer = WatchListSerializer(instance=watch_list, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response({"message": "Failed to update data"}, status=status.HTTP_417_EXPECTATION_FAILED)
