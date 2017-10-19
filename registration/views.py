from django.core.mail import EmailMessage

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from registration.models import Registration
from registration.serializers import RegistrationSerializer
from registration.serializers import RegistrationSerializer2

class RegistrationList(APIView):
    def get(self, request, format=None):
        permission_classes = (IsAuthenticated,)

        registrations = Registration.objects.all()
        serializer = RegistrationSerializer2(registrations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        permission_classes = (IsAuthenticated,)

        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email_address = request.data["email"]
            self.send_verfication(email_address)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_verfication(self, email_address):
        title = "Tervetuloa Stimulaatioon 1.12.2017"
        body = """Tervetuloa Stimulaatioon,

Tämä on vahvistus ilmoittautumisestasi Automaatio- ja systeemitekniikan killan vuosijuhlaan Stimulaatioon. Tässä sähköpostissa vielä muutama käytännön ohje juhlaan liittyen.

Juhlat pidetään 1. joulukuuta ja ne alkavat kello 16:00 cocktailtilaisuudella TUAS-talolla osoitteessa Maarintie 8, 02150 Espoo. Mikäli olet ilmoittaunut antamaan tervehdyksen muista olla paikalla ajoissa. TUAS-talolta on kuljetukset pääjuhlapaikalle Kauniaisten VPK-talolle (Asematie 20, 02700 Kauniainen), jossa pöytäjuhla alkaa kello 19:00. Pöytäosuuden jälkeen seuraa wanhat tanssit sekä vapaammat jatkot, jonne on kuljetukset pääjuhlapaikalta.

Silliaamiainen Stillis käynnistää seuraavan päivän Otaniemen Rantasaunalla (Vastaranta 1, 02150 Espoo) ja paikalle voi saapua kello 12:00 alkaen.

Juhlan maksutiedot ovat seuraavat:

Saaja: Automaatio- ja systeemitekniikan kilta ry
IBAN: FI84 3131 3001 8081 61
Viesti: Stimulaatio 2017, "Oma Nimi"
Hinta: 75 € (opiskelija) tai 90 € (valmistunut), Stillis 15 €
Eräpäivä: 19.11.2017

Allekirjoittanut vastaa mielellään juhliin liittyviin kysymyksiin.

--
Ystävällisin terveisin,

Paul laihonen
Stimulantti
stimulantti@as.fi
"""
        verification_email = EmailMessage(title, body, to=[email_address])
        verification_email.send()


class RegistrationListAll(APIView):
    def get(self, request, format=None):
        permission_classes = (IsAuthenticated,)

        registrations = Registration.objects.all()
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)


class RegistrationDetail(APIView):
    def get_object(selk, pk):
        permission_classes = (IsAuthenticated,)

        try:
            registration = Registration.objects.get(pk=pk)
        except Registration.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        permission_classes = (IsAuthenticated,)

        registration = self.get_object(pk)
        serializer = RegistrationSerializer(registration)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        permission_classes = (IsAuthenticated,)

        registration = self.get_object(pk)
        serializer = RegistrationSerializer(registration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ok, format=None):
        permission_classes = (IsAuthenticated,)

        registration = self.get_object(pk)
        registration.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
