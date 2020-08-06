from rest_framework import serializers
from registration.models import Registration

class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = ('id', 'first_name', 'last_name', 'email', 'is_invited', 'ticket_type', 'sillis', 'table_company', 'avec', 'special_diet', 'menu_type', 'greeting', 'freshman_year', 'greeting_group', 'show_name')

class RegistrationSerializer2(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = ('id', 'first_name', 'last_name', 'table_company')
