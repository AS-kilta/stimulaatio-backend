from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from registration.models import Registration
from registration.serializers import RegistrationSerializer
from registration.serializers import RegistrationSerializer2


class RegistrationList(APIView):
    def get(self, request, format=None):
        registrations = Registration.objects.all()
        serializer = RegistrationSerializer2(registrations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrationListAll(APIView):
    def get(self, request, format=None):
        registrations = Registration.objects.all()
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)


class RegistrationDetail(APIView):
    def get_object(selk, pk):
        try:
            registration = Registration.objects.get(pk=pk)
        except Registration.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        registration = self.get_object(pk)
        serializer = RegistrationSerializer(registration)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        registration = self.get_object(pk)
        serializer = RegistrationSerializer(registration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ok, format=None):
        registration = self.get_object(pk)
        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
