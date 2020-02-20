from dateutil.parser import parser
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils import formats

from utenti.models import Profile
from annunci.models import Annuncio, Servizio



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        exclude=[
                "last_login",
                "is_superuser",
                "is_staff",
                "is_active",
                "date_joined",
                "groups",
                "user_permissions",
                ]
        read_only_fields = ["id"]
        # fields = [  "id",
        #             "username",
        #             "first_name",
        #             "last_name",
        #             "email"]
        # extra_kwargs = {
        #                 'username': {
        #                     'validators': [UnicodeUsernameValidator()],
        #                 }
        # }

class AnagraficaSerializer(serializers.ModelSerializer):
    '''
    classe per effettuare la serializzazione dei dati.
    I Serializers permettono la conversione di tipi di dato complessi come :
    istanze di modelli o queryset in tipi di dato nativi di Python,
    facilitandone il rendering in formati a noi utili come ad esempio JSON
    '''

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields =["id"]
        # exclude = ("latitudine", "longitudine","pet_coins", "pet_sitter", "id", "user")
        # read_only_fields = ['user',"latitudine", "longitudine","pet_coins", "pet_sitter", "id"]


class DatiUtenteCompleti(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = Profile
        fields = "__all__"

    def update(self, instance, validated_data):
        v = instance.user.username
        print(v)
        dati_utente= validated_data.pop('user')
        print("dati_utente",dati_utente)
        utente_richiedente = Profile.objects.get(user=instance.user)
        print("utente richiedente ",utente_richiedente)
        # username, first_name, last_name, email
        print("validated_data",validated_data)
        instance.user.username = dati_utente['username']
        instance.user.set_password(dati_utente['password'])
        instance.user.first_name = dati_utente['first_name']
        instance.user.last_name = dati_utente['last_name']
        instance.user.email = dati_utente['email']


        instance.indirizzo = validated_data['indirizzo']
        instance.citta =  validated_data['citta']
        instance.regione =  validated_data['regione']
        instance.provincia =  validated_data['provincia']
        instance.latitudine =  validated_data['latitudine']
        instance.longitudine =validated_data['longitudine']
        instance.telefono =validated_data['telefono']
        instance.pet_coins =validated_data['pet_coins']
        instance.foto_profilo =validated_data['foto_profilo']
#         controllo il tipo di utente

        if utente_richiedente.pet_sitter == False:
            print("pet sitter FALSE")
            instance.pet_sitter=False
            instance.nome_pet = validated_data['nome_pet']
            instance.pet = validated_data['pet']
            instance.razza = validated_data['razza']
            instance.eta = validated_data['eta']
            instance.caratteristiche = validated_data['caratteristiche']
            instance.foto_pet = validated_data['foto_pet']
        else:
            print("pet sitter TRUE")
            instance.pet_sitter=True

        instance.descrizione = validated_data['descrizione']
        instance.hobby = validated_data['hobby']
        instance.user.save()
        instance.save()
        return instance







# class DateTimeFieldWihTZ(serializers.DateTimeField):
#     '''Class to make output of a DateTime Field timezone aware
#     '''
#     def to_representation(self, value):
#         value = timezone.localtime(value)
#         return super(DateTimeFieldWihTZ, self).to_representation(value)
#
#
# class CustomDateTimeField(serializers.DateTimeField):
#     def to_representation(self, value):
#         print("value ", value)
#         tz = timezone.get_default_timezone()
#         # timezone.localtime() defaults to the current tz, you only
#         # need the `tz` arg if the current tz != default tz
#         value = timezone.localtime(value, timezone=tz)
#         # py3 notation below, for py2 do:
#         return super(CustomDateTimeField, self).to_representation(value)
#         # return super().to_representation(value)


class AnnuncioSerializer(serializers.ModelSerializer):
    # data_inizio = DateTimeFieldWihTZ(format='%Y-%m-%d %H:%M', input_formats=['%Y-%m-%dT%H:%M:%SZ',])
    # data_fine = DateTimeFieldWihTZ(format='%Y-%m-%d %H:%M', input_formats=['%Y-%m-%dT%H:%M:%SZ',])

    # "modo usaro da django": "2020-02-29T15:12:00",
    # "modo usato da django rest": "2020-02-08T16:49:50.590558",

    # data_inizio = CustomDateTimeField()
    # data_fine = CustomDateTimeField()

    data_inizio =serializers.DateTimeField(format=None,input_formats=None)
    data_fine =serializers.DateTimeField(format=None,input_formats=None)

    class Meta:
        model = Annuncio
        fields = "__all__"
        read_only_fields = ("id",)


class ServizioOffertoSerializer(serializers.ModelSerializer):
    # annuncio = AnnuncioSerializer(many=False)
    class Meta:
        model = Servizio
        fields = "__all__"

class AnnuncioConServizi(serializers.ModelSerializer):
    annuncio = AnnuncioSerializer(many=False)
    class Meta:
        model = Servizio
        fields = "__all__"
    def create(self, validated_data):
        dati_annuncio = validated_data.pop('annuncio')
        print(validated_data)
        print(dati_annuncio)
        print(dati_annuncio['user'])
        annuncio_nuovo=Annuncio.objects.create(user=dati_annuncio['user'])

        annuncio_nuovo.user = dati_annuncio['user']

        userprofile = Profile.objects.filter(user=dati_annuncio['user']).first()

        print("userprofile",userprofile)
        if userprofile.pet_sitter:
            annuncio_nuovo.annuncio_petsitter=True
        else:
            annuncio_nuovo.annuncio_petsitter=False

        annuncio_nuovo.titolo = dati_annuncio['titolo']
        annuncio_nuovo.sottotitolo = dati_annuncio['sottotitolo']
        annuncio_nuovo.descrizione = dati_annuncio['descrizione']
        annuncio_nuovo.pet = dati_annuncio['pet']
        annuncio_nuovo.pet_coins = dati_annuncio['pet_coins']
        annuncio_nuovo.data_inizio = dati_annuncio['data_inizio']
        annuncio_nuovo.data_fine = dati_annuncio['data_fine']
        annuncio_nuovo.logo_annuncio = dati_annuncio['logo_annuncio']
        annuncio_nuovo.save()

        servizi = Servizio.objects.create(annuncio=annuncio_nuovo)
        servizi.passeggiate = validated_data['passeggiate']
        servizi.pulizia_gabbia = validated_data['pulizia_gabbia']
        servizi.ore_compagnia = validated_data['ore_compagnia']
        servizi.cibo = validated_data['cibo']
        servizi.accompagna_dal_vet = validated_data['accompagna_dal_vet']
        servizi.save()

        return servizi

# class CalendarioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Annuncio
#         fields = "__all__"
#         read_only_fields = ("id",)