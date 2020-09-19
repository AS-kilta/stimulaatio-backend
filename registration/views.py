from django.core.mail import EmailMessage

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from registration.models import Registration
from registration.serializers import RegistrationSerializer
from registration.serializers import RegistrationSerializer2

class RegistrationList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        registrations = Registration.objects.all().filter(show_name=True).order_by('id')
        serializer = RegistrationSerializer2(registrations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            self.generate_verification_email(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def generate_verification_email(self, registration_data):

        # Hard coded email title
        title = "Tervetuloa Stimulaatioon 13.11.2020"

        with open('email.txt', 'r') as email_file:
            confirmation_email = email_file.read()

        # Nimi
        confirmation_email = confirmation_email.replace("${name}", registration_data["first_name"] + " " + registration_data["last_name"])

        # Sähköposti
        confirmation_email = confirmation_email.replace("${email}", registration_data["email"])

        # Lipputyyppi
        if registration_data["ticket_type"] == "free":
            confirmation_email = confirmation_email.replace("${ticket_type}", "Tarjottu")
        elif registration_data["ticket_type"] == "student":
            confirmation_email = confirmation_email.replace("${ticket_type}", "Opiskelija")
        elif registration_data["ticket_type"] == "full":
            confirmation_email = confirmation_email.replace("${ticket_type}", "Valmistunut")

        # Sillis
        # if registration_data["sillis"]:
        #     confirmation_email = confirmation_email.replace("${sillis}", "Kyllä")
        # else:
        #     confirmation_email = confirmation_email.replace("${sillis}", "Ei")
        # email.txt tiedostoon tulee lisätä kohta sillikselle, jos tämän haluaa mukaan 

        # Pöytäseura
        confirmation_email = confirmation_email.replace("${table_company}", registration_data["table_company"])

        # Avec
        confirmation_email = confirmation_email.replace("${avec}", registration_data["avec"])

        # Erikoisruokavalio
        confirmation_email = confirmation_email.replace("${special_diet}", registration_data["special_diet"])

        # Menu
        if registration_data["menu_type"] == "with alcohol":
            confirmation_email = confirmation_email.replace("${menu_type}", "Alkoholillinen")
        else:
            confirmation_email = confirmation_email.replace("${menu_type}", "Alkoholiton")

        # Kutsuvieras
        if registration_data["is_invited"]:
            confirmation_email = confirmation_email.replace("${is_invited}", "Kyllä")
        else:
            confirmation_email = confirmation_email.replace("${is_invited}", "Ei")

        # Tervehdys
        if registration_data["greeting"]:
            confirmation_email = confirmation_email.replace("${greeting}", "Kyllä")
        else:
            confirmation_email = confirmation_email.replace("${greeting}", "Ei")

        # Edustettu taho
        if registration_data["is_invited"] or registration_data["greeting"]:
            confirmation_email = confirmation_email.replace("${greeting_group}", "Edustettu taho: " + registration_data["greeting_group"] + "\n")
        else:
            confirmation_email = confirmation_email.replace("${greeting_group}", "")

        # Phuksivuosi
        confirmation_email = confirmation_email.replace("${freshman_year}", registration_data["freshman_year"])

        # Tietojen julkisuus
        if registration_data["show_name"]:
            confirmation_email = confirmation_email.replace("${show_name}", "Saa julkaista")
        else:
            confirmation_email = confirmation_email.replace("${show_name}", "Ei saa julkaista")

        self.send_verfication(registration_data["email"], title, confirmation_email)

    def send_verfication(self, email_address, title, message):
        verification_email = EmailMessage(title, message, to=[email_address])
        verification_email.send()


class RegistrationListAll(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        registrations = Registration.objects.all()
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)


class RegistrationDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return Registration.objects.get(pk=pk)
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

    def delete(self, request, pk, format=None):
        registration = self.get_object(pk)
        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegistrationCount(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        count = Registration.objects.all().count()
        return Response(count)
