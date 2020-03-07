from dateutil.parser import parser
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
import datetime
from django.utils import timezone
from django.utils import formats
import magic
from static import NamingList
import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from recensioni.models import Recensione
from utenti.models import Profile
from annunci.models import Annuncio, Servizio
from utenti.views import calcola_lat_lon

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
MIME_TYPES = ['image/jpeg', 'image/png']
CONTENT_TYPES = ['image', 'video']
MAX_UPLOAD_SIZE = "5242880"

def aggiornaLatLng(user, request):
    utente_richiedente = Profile.objects.get(user=user)
    latitudine, longitudine = calcola_lat_lon(request, utente_richiedente)
    print(latitudine, longitudine)
    utente_richiedente.latitudine = latitudine
    utente_richiedente.longitudine = longitudine
    utente_richiedente.save()


def calcolaMediaVotiUtente(profilo):
    utente = User.objects.get(username = profilo)
    somma = 0
    recensioni = Recensione.objects.filter(user_recensito=utente)
    # print("recensioni : ",recensioni)
    for obj in recensioni:
        somma += obj.voto
    if len(recensioni)!=0:
        media = somma / len(recensioni)
    else:
        media = 0
    return media

def calcolaNumeroVotiUtente(profilo):
    utente = User.objects.get(username = profilo)
    recensioni = Recensione.objects.filter(user_recensito=utente)
    return len(recensioni)

class UsernameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username"]

    def validate_username(self, data):
        if not re.match("^[A-Za-z0-9]+$", data):
            return serializers.ValidationError(
                _('Errore: lo username può contenere solo lettere e numeri.'))
        if not (3 <= len(data) <= 30):
            return serializers.ValidationError(
                _('Errore: lo username deve avere lunghezza fra 3 e 30 caratteri.'))
        return data['username']


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
        extra_kwargs = {
                        'username': {
                            'validators': [UnicodeUsernameValidator()],
                        }
        }

        def validate_username(self, data):
            if not re.match("^[A-Za-z0-9]+$", data):
                return serializers.ValidationError(
                    _('Errore: lo username può contenere solo lettere e numeri.'))
            if not (3 <= len(data) <= 30):
                return serializers.ValidationError(
                    _('Errore: lo username deve avere lunghezza fra 3 e 30 caratteri.'))
            return data['username']

        def validate_password(self, data):
            # controllo password
            if not re.match("^[A-Za-z0-9èòàùì]+$", data):
                raise serializers.ValidationError(
                    _('Errore: la password può contenere solo lettere minuscole, maiuscole e numeri.'))
            if not (3 <= len(data) <= 20):
                raise serializers.ValidationError(
                    _('Errore: la password deve avere lunghezza fra 3 e 20 caratteri.'))
            return data

        def validate_conferma_password(self, data):
            if not re.match("^[A-Za-z0-9èòàùì]+$", data):
                raise serializers.ValidationError(
                    _('Errore: la conferma password può contenere solo lettere minuscole, maiuscole e numeri.'))
            if not (3 <= len(data) <= 20):
                raise serializers.ValidationError(
                    _('Errore: la conferma password deve avere lunghezza fra 3 e 20 caratteri.'))
            return data

        def validate_first_name(self,data):
            if not re.match("^[A-Za-z 'èòàùì]+$", data):
                raise serializers.ValidationError(_('Errore: il nome può contenere solo lettere.'))
            if not (1 <= len(data) <= 30):
                raise ValidationError(_('Errore: il nome deve avere lunghezza fra 1 e 30 caratteri.'))
            return data

        def validate_last_name(self,data):
            # controllo cognome
            if not re.match("^[A-Za-z 'èòàùì]+$", data):
                raise serializers.ValidationError(_('Errore: il cognome può contenere solo lettere.'))
            if not (1 <= len(data) <= 30):
                raise serializers.ValidationError(_('Errore: il cognome deve avere lunghezza fra 1 e 30 caratteri.'))
            return data

        def validate_email(self,data):
            # controllo email
            if not (5 <= len(data) <= 50):
                raise serializers.ValidationError(_('Errore: la mail deve essere compresa gra 5 e 50 caratteri.'))
            return data




class AnagraficaSerializer(serializers.ModelSerializer):
    '''
    classe per effettuare la serializzazione dei dati.
    I Serializers permettono la conversione di tipi di dato complessi come :
    istanze di modelli o queryset in tipi di dato nativi di Python,
    facilitandone il rendering in formati a noi utili come ad esempio JSON
    '''
    foto_profilo = serializers.FileField(read_only=True)
    foto_pet = serializers.FileField(read_only=True)
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields =["id"]
        # exclude = ("latitudine", "longitudine","pet_coins", "pet_sitter", "id", "user")
        # read_only_fields = ['user',"latitudine", "longitudine","pet_coins", "pet_sitter", "id"]

    def validate_indirizzo(self,data):
        # controllo indirizzo
        if not re.match("^[A-Za-z0-9/ 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: l\'indirizzo può contenere solo lettere, numeri e /.'))
        if not (3 <= len(data) <= 50):
            raise serializers.ValidationError(
                _('Errore: l\'indirizzo deve avere lunghezza fra 3 e 50 caratteri.'))
        return data

    def validate_citta(self, data):
        # controllo citta
        if not re.match("^[A-Za-z 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo città può contenere solo lettere.'))
        if not (3 <= len(data) <= 50):
            raise serializers.ValidationError(
                _('Errore: la città deve avere lunghezza fra 3 e 50 caratteri.'))
        return data

    def validate_telefono(self, data):
        # controllo telefono
        if not re.match("^[0-9]+$", data):
            raise serializers.ValidationError(
                _('Errore: il telefono può contenere solo numeri.'))
        if not (3 <= len(data) <= 30):
            raise serializers.ValidationError(
                _('Errore: il telefono deve avere lunghezza fra 3 e 30 caratteri.'))
        return data

    def validate_foto_profilo(self,data):
        files = data

        if files is not None:

            file_size = files.size
            limit_MB = 5
            if file_size > limit_MB * 1024 * 1024:
                raise serializers.ValidationError("La dimensione massima per le immagini è %s MB" % limit_MB)

            file_type = magic.from_buffer(files.read(), mime=True)
            if file_type not in MIME_TYPES:
                raise serializers.ValidationError(_("file non supportato."))
            return files
        return None

    def validate_nome_pet(self, data):
        if not re.match("^[A-Za-z 'èòàùì]+$", data):
            raise serializers.ValidationError(_('Errore: il nome del pet può contenere solo lettere.'))
        if not (3 <= len(data) <= 30):
            raise serializers.ValidationError(
                _('Errore: il nome del pet deve avere lunghezza fra 3 e 30 caratteri.'))
        return data

    def validate_razza(self, data):
        # controllo razza
        if not re.match("^[A-Za-z -'èòàùì]+$", data):
            raise serializers.ValidationError(_('Errore: la razza del pet può contenere solo lettere e spazi.'))
        if not (3 <= len(data) <= 30):
            raise serializers.ValidationError(
                _('Errore: la razza del pet deve avere lunghezza fra 3 e 30 caratteri.'))
        return data

    def validate_caratteristiche(self, data):
        # controllo caratteristiche
        if not re.match("^[A-Za-z0-9., 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo caratteristiche può contenere solo lettere, numeri, punti, virgole e spazi.'))
        if not (1 <= len(data) <= 245):
            raise serializers.ValidationError(
                _('Errore: il campo caratteristiche deve avere lunghezza fra 1 e 245 caratteri.'))
        return data

    def validate_foto_pet(self, data):
        files = data
        if files is not None:
            file_size = files.size
            limit_MB = 5
            if file_size > limit_MB * 1024 * 1024:
                raise serializers.ValidationError("La dimensione massima per le immagini è %s MB" % limit_MB)

            file_type = magic.from_buffer(files.read(), mime=True)
            if file_type not in MIME_TYPES:
                raise serializers.ValidationError(_("file non supportato."))
            return files
        return None

    def validate_descrizione(self, data):
        # controllo descrizione
        if not re.match("^[A-Za-z0-9., 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo descrizione può contenere solo lettere, numeri, punti, virgole e spazi.'))
        if not (1 <= len(data) <= 245):
            raise serializers.ValidationError(
                _('Errore: il campo descrizione deve avere lunghezza fra 1 e 245 caratteri.'))
        return data

    def validate_hobby(self, data):
        # controllo hobby
        if not re.match("^[A-Za-z0-9., 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo hobby può contenere solo lettere, numeri, punti, virgole e spazi.'))
        if not (1 <= len(data) <= 95):
            raise serializers.ValidationError(
                _('Errore: il campo hobby deve avere lunghezza fra 1 e 95 caratteri.'))
        return data

    def validate_eta(self, data):
        # controllo eta
        if not re.match("^[0-9]+$", str(data)):
            raise serializers.ValidationError(_('Errore: l\'età può contenere solo numeri.'))
        if not (0 <= int(data) <= 100):
            raise serializers.ValidationError(_('Errore: l\'età deve essere compresa fra 0 e 100.'))
        return data





class RecensioniSerializer(serializers.ModelSerializer):
    user_recensore = serializers.CharField(max_length=30, allow_null=True, allow_blank=True, required=False)
    user_recensito = serializers.CharField(max_length=30, allow_null=True, allow_blank=True, required=False)
    class Meta:
        model = Recensione
        fields ='__all__'
        # fields =['titolo',
        #          'descrizione',
        #          'voto'
        #          ]

    def validate_descrizione(self, data):
        # controllo descrizione
        if not re.match("^[A-Za-z0-9 ,.'èòàùì]+$", data):
            raise serializers.ValidationError(_('Errore: la descrizione può contenere solo lettere, '
                                               'numeri, punti, virgole e spazi.'))
        return data

    def validate_titolo(self, data):
        if not re.match("^[A-Za-z0-9 .,'èòàùì]+$", data):
            raise serializers.ValidationError(_('Errore: il titolo può contenere solo lettere, numeri e spazi.'))
        if not (1 <= len(data) <= 95):
            raise serializers.ValidationError(_('Errore: il titolo deve avere lunghezza fra 1 e 95 caratteri.'))
        return data


class DatiUtenteCompleti(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    numero_recensioni = serializers.SerializerMethodField("get_numero_recensioni_utente")
    media_voti = serializers.SerializerMethodField("get_media_voti_utente")
    foto_profilo = serializers.FileField(read_only=True)
    foto_pet = serializers.FileField(read_only=True)
    class Meta:
        model = Profile
        fields =["user",
                 "indirizzo",
                 "citta",
                 "provincia",
                 "regione",
                 "telefono",
                 "pet_coins",
                 "foto_profilo",
                 "pet_sitter",
                 "nome_pet",
                 "pet",
                 "razza",
                 "eta",
                 "caratteristiche",
                 "foto_pet",
                 "descrizione",
                 "hobby",
                 "numero_recensioni",
                 "media_voti",
                 ]

    def validate_indirizzo(self,data):
        # controllo indirizzo
        if not re.match("^[A-Za-z0-9/ 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: l\'indirizzo può contenere solo lettere, numeri e /.'))
        if not (3 <= len(data) <= 50):
            raise serializers.ValidationError(
                _('Errore: l\'indirizzo deve avere lunghezza fra 3 e 50 caratteri.'))
        return data

    def validate_citta(self, data):
        # controllo citta
        if not re.match("^[A-Za-z 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo città può contenere solo lettere.'))
        if not (3 <= len(data) <= 50):
            raise serializers.ValidationError(
                _('Errore: la città deve avere lunghezza fra 3 e 50 caratteri.'))
        return data

    def validate_telefono(self, data):
        # controllo telefono
        if not re.match("^[0-9]+$", data):
            raise serializers.ValidationError(
                _('Errore: il telefono può contenere solo numeri.'))
        if not (3 <= len(data) <= 30):
            raise serializers.ValidationError(
                _('Errore: il telefono deve avere lunghezza fra 3 e 30 caratteri.'))
        return data

    def validate_foto_profilo(self,data):
        files = data

        if files is not None:
            file_size = files.size
            limit_MB = 5
            if file_size > limit_MB * 1024 * 1024:
                raise serializers.ValidationError("La dimensione massima per le immagini è %s MB" % limit_MB)

            file_type = magic.from_buffer(files.read(), mime=True)
            if file_type not in MIME_TYPES:
                raise serializers.ValidationError(_("file non supportato."))
            return files
        return None

    def validate_nome_pet(self, data):
        if not re.match("^[A-Za-z 'èòàùì]+$", data):
            raise serializers.ValidationError(_('Errore: il nome del pet può contenere solo lettere.'))
        if not (3 <= len(data) <= 30):
            raise serializers.ValidationError(
                _('Errore: il nome del pet deve avere lunghezza fra 3 e 30 caratteri.'))
        return data

    def validate_razza(self, data):
        # controllo razza
        if not re.match("^[A-Za-z -'èòàùì]+$", data):
            raise serializers.ValidationError(_('Errore: la razza del pet può contenere solo lettere e spazi.'))
        if not (3 <= len(data) <= 30):
            raise serializers.ValidationError(
                _('Errore: la razza del pet deve avere lunghezza fra 3 e 30 caratteri.'))
        return data

    def validate_caratteristiche(self, data):
        # controllo caratteristiche
        if not re.match("^[A-Za-z0-9., 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo caratteristiche può contenere solo lettere, numeri, punti, virgole e spazi.'))
        if not (1 <= len(data) <= 245):
            raise serializers.ValidationError(
                _('Errore: il campo caratteristiche deve avere lunghezza fra 1 e 245 caratteri.'))
        return data

    def validate_foto_pet(self, data):
        files = data
        if files is not None:
            file_size = files.size
            limit_MB = 5
            if file_size > limit_MB * 1024 * 1024:
                raise serializers.ValidationError("La dimensione massima per le immagini è %s MB" % limit_MB)

            file_type = magic.from_buffer(files.read(), mime=True)
            if file_type not in MIME_TYPES:
                raise serializers.ValidationError(_("file non supportato."))
            return files
        return None

    def validate_descrizione(self, data):
        # controllo descrizione
        if not re.match("^[A-Za-z0-9., 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo descrizione può contenere solo lettere, numeri, punti, virgole e spazi.'))
        if not (1 <= len(data) <= 245):
            raise serializers.ValidationError(
                _('Errore: il campo descrizione deve avere lunghezza fra 1 e 245 caratteri.'))
        return data

    def validate_hobby(self, data):
        # controllo hobby
        if not re.match("^[A-Za-z0-9., 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo hobby può contenere solo lettere, numeri, punti, virgole e spazi.'))
        if not (1 <= len(data) <= 95):
            raise serializers.ValidationError(
                _('Errore: il campo hobby deve avere lunghezza fra 1 e 95 caratteri.'))
        return data

    def validate_eta(self, data):
        # controllo eta
        if not re.match("^[0-9]+$", str(data)):
            raise serializers.ValidationError(_('Errore: l\'età può contenere solo numeri.'))
        if not (0 <= int(data) <= 100):
            raise serializers.ValidationError(_('Errore: l\'età deve essere compresa fra 0 e 100.'))
        return data

    def get_media_voti_utente(self,profilo):
        # user = Profile.__class__.objects.get(user=self.instance)
        return calcolaMediaVotiUtente(profilo)


    def get_numero_recensioni_utente(self,profilo):
        # user = Profile.__class__.objects.get(user=self.instance)
        return calcolaNumeroVotiUtente(profilo)

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
        # instance.latitudine =  validated_data['latitudine']
        # instance.longitudine =validated_data['longitudine']
        instance.telefono =validated_data['telefono']
        instance.pet_coins =validated_data['pet_coins']
        # instance.foto_profilo =validated_data['foto_profilo']
#         controllo il tipo di utente

        if utente_richiedente.pet_sitter == False:
            print("pet sitter FALSE")
            instance.pet_sitter=False
            instance.nome_pet = validated_data['nome_pet']
            instance.pet = validated_data['pet']
            instance.razza = validated_data['razza']
            instance.eta = validated_data['eta']
            instance.caratteristiche = validated_data['caratteristiche']
            # instance.foto_pet = validated_data['foto_pet']
        else:
            print("pet sitter TRUE")
            instance.pet_sitter=True
            instance.descrizione = validated_data['descrizione']
            instance.hobby = validated_data['hobby']

        instance.user.save()
        instance.save()
        aggiornaLatLng(instance.user, self.context['request'])

        # utente_richiedente = Profile.objects.get(user=instance.user)
        # latitudine, longitudine = calcola_lat_lon(self.context['request'], utente_richiedente)
        # print(latitudine,longitudine)
        # utente_richiedente.latitudine = latitudine
        # utente_richiedente.longitudine = longitudine
        # utente_richiedente.save()

        return instance




class CompletaDatiDjangoUser(serializers.ModelSerializer):
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
        read_only_fields = ["id", "email", "username", "password"]


        def validate_first_name(self,data):
            if not re.match("^[A-Za-z 'èòàùì]+$", data):
                raise serializers.ValidationError(_('Errore: il nome può contenere solo lettere.'))
            if not (1 <= len(data) <= 30):
                raise ValidationError(_('Errore: il nome deve avere lunghezza fra 1 e 30 caratteri.'))
            return data

        def validate_last_name(self,data):
            # controllo cognome
            if not re.match("^[A-Za-z 'èòàùì]+$", data):
                raise serializers.ValidationError(_('Errore: il cognome può contenere solo lettere.'))
            if not (1 <= len(data) <= 30):
                raise serializers.ValidationError(_('Errore: il cognome deve avere lunghezza fra 1 e 30 caratteri.'))
            return data




class CompletaRegPetsitterSerializer(serializers.ModelSerializer):
    user = CompletaDatiDjangoUser(many=False)
    foto_profilo = serializers.FileField(read_only=True)
    class Meta:
        model = Profile
        exclude = ("pet_coins",
                   "pet_sitter",
                   "id",
                   'nome_pet',
                   'pet',
                   'razza',
                   'eta',
                   'caratteristiche',
                   'foto_pet',
                   "latitudine",
                   "longitudine",
                   )

    def validate_indirizzo(self,data):
        # controllo indirizzo
        if not re.match("^[A-Za-z0-9/ 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: l\'indirizzo può contenere solo lettere, numeri e /.'))
        if not (3 <= len(data) <= 50):
            raise serializers.ValidationError(
                _('Errore: l\'indirizzo deve avere lunghezza fra 3 e 50 caratteri.'))
        return data

    def validate_citta(self, data):
        # controllo citta
        if not re.match("^[A-Za-z 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo città può contenere solo lettere.'))
        if not (3 <= len(data) <= 50):
            raise serializers.ValidationError(
                _('Errore: la città deve avere lunghezza fra 3 e 50 caratteri.'))
        return data

    def validate_telefono(self, data):
        # controllo telefono
        if not re.match("^[0-9]+$", data):
            raise serializers.ValidationError(
                _('Errore: il telefono può contenere solo numeri.'))
        if not (3 <= len(data) <= 30):
            raise serializers.ValidationError(
                _('Errore: il telefono deve avere lunghezza fra 3 e 30 caratteri.'))
        return data

    def validate_foto_profilo(self,data):
        files = data

        if files is not None:
            file_size = files.size
            limit_MB = 5
            if file_size > limit_MB * 1024 * 1024:
                raise serializers.ValidationError("La dimensione massima per le immagini è %s MB" % limit_MB)

            file_type = magic.from_buffer(files.read(), mime=True)
            if file_type not in MIME_TYPES:
                raise serializers.ValidationError(_("file non supportato."))
            return files
        return None

    def validate_descrizione(self, data):
        # controllo descrizione
        if not re.match("^[A-Za-z0-9., 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo descrizione può contenere solo lettere, numeri, punti, virgole e spazi.'))
        if not (1 <= len(data) <= 245):
            raise serializers.ValidationError(
                _('Errore: il campo descrizione deve avere lunghezza fra 1 e 245 caratteri.'))
        return data

    def validate_hobby(self, data):
        # controllo hobby
        if not re.match("^[A-Za-z0-9., 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo hobby può contenere solo lettere, numeri, punti, virgole e spazi.'))
        if not (1 <= len(data) <= 95):
            raise serializers.ValidationError(
                _('Errore: il campo hobby deve avere lunghezza fra 1 e 95 caratteri.'))
        return data


    def update(self, instance, validated_data):
        v = instance.user.username
        print(v)
        dati_utente= validated_data.pop('user')
        print("dati_utente",dati_utente)
        utente_richiedente = Profile.objects.get(user=instance.user)
        print("utente richiedente ",utente_richiedente)
        # username, first_name, last_name, email
        print("validated_data",validated_data)
        # instance.user.username = dati_utente['username']
        # instance.user.set_password(dati_utente['password'])
        instance.user.first_name = dati_utente['first_name']
        instance.user.last_name = dati_utente['last_name']
        # instance.user.email = dati_utente['email']
        instance.indirizzo = validated_data['indirizzo']
        instance.citta =  validated_data['citta']
        instance.regione =  validated_data['regione']
        instance.provincia =  validated_data['provincia']

        # instance.latitudine =  validated_data['latitudine']
        # instance.longitudine =validated_data['longitudine']

        instance.telefono =validated_data['telefono']
        # instance.pet_coins =validated_data['pet_coins']
        # instance.foto_profilo =validated_data['foto_profilo']

        instance.pet_sitter=True

        instance.descrizione = validated_data['descrizione']
        instance.hobby = validated_data['hobby']
        instance.user.save()
        instance.save()

        aggiornaLatLng(instance.user, self.context['request'])

        # latitudine , longitudine =  calcola_lat_lon(self.context['request'], utente_richiedente)
        # utente_richiedente.latitudine = latitudine
        # utente_richiedente.longitudine = longitudine
        # utente_richiedente.save()

        return instance

class CompletaRegUtenteNormale(serializers.ModelSerializer):
    user = CompletaDatiDjangoUser(many=False)
    foto_profilo = serializers.FileField(read_only=True)
    foto_pet = serializers.FileField(read_only=True)
    class Meta:
        model = Profile
        # fields = "__all__"
        exclude = ("latitudine",
                   "longitudine",
                   "pet_coins",
                   "pet_sitter",
                   "id",
                   "descrizione",
                   "hobby",
                   )

    def validate_indirizzo(self,data):
        # controllo indirizzo
        if not re.match("^[A-Za-z0-9/ 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: l\'indirizzo può contenere solo lettere, numeri e /.'))
        if not (3 <= len(data) <= 50):
            raise serializers.ValidationError(
                _('Errore: l\'indirizzo deve avere lunghezza fra 3 e 50 caratteri.'))
        return data

    def validate_citta(self, data):
        # controllo citta
        if not re.match("^[A-Za-z 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo città può contenere solo lettere.'))
        if not (3 <= len(data) <= 50):
            raise serializers.ValidationError(
                _('Errore: la città deve avere lunghezza fra 3 e 50 caratteri.'))
        return data

    def validate_telefono(self, data):
        # controllo telefono
        if not re.match("^[0-9]+$", data):
            raise serializers.ValidationError(
                _('Errore: il telefono può contenere solo numeri.'))
        if not (3 <= len(data) <= 30):
            raise serializers.ValidationError(
                _('Errore: il telefono deve avere lunghezza fra 3 e 30 caratteri.'))
        return data

    def validate_foto_profilo(self,data):
        files = data

        if files is not None:
            file_size = files.size
            limit_MB = 5
            if file_size > limit_MB * 1024 * 1024:
                raise serializers.ValidationError("La dimensione massima per le immagini è %s MB" % limit_MB)

            file_type = magic.from_buffer(files.read(), mime=True)
            if file_type not in MIME_TYPES:
                raise serializers.ValidationError(_("file non supportato."))
            return files
        return None

    def validate_nome_pet(self, data):
        if not re.match("^[A-Za-z 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il nome del pet può contenere solo lettere.'))
        if not (3 <= len(data) <= 30):
            raise serializers.ValidationError(
                _('Errore: il nome del pet deve avere lunghezza fra 3 e 30 caratteri.'))
        return data

    def validate_razza(self, data):
        # controllo razza
        if not re.match("^[A-Za-z -'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: la razza del pet può contenere solo lettere e spazi.'))
        if not (3 <= len(data) <= 30):
            raise serializers.ValidationError(
                _('Errore: la razza del pet deve avere lunghezza fra 3 e 30 caratteri.'))
        return data

    def validate_caratteristiche(self, data):
        # controllo caratteristiche
        if not re.match("^[A-Za-z0-9., 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo caratteristiche può contenere solo lettere, numeri, punti, virgole e spazi.'))
        if not (1 <= len(data) <= 245):
            raise serializers.ValidationError(
                _('Errore: il campo caratteristiche deve avere lunghezza fra 1 e 245 caratteri.'))
        return data

    def validate_foto_pet(self, data):
        files = data
        if files is not None:
            file_size = files.size
            limit_MB = 5
            if file_size > limit_MB * 1024 * 1024:
                raise serializers.ValidationError("La dimensione massima per le immagini è %s MB" % limit_MB)

            file_type = magic.from_buffer(files.read(), mime=True)
            if file_type not in MIME_TYPES:
                raise serializers.ValidationError(_("file non supportato."))
            return files
        return None

    def validate_descrizione(self, data):
        # controllo descrizione
        if not re.match("^[A-Za-z0-9., 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo descrizione può contenere solo lettere, numeri, punti, virgole e spazi.'))
        if not (1 <= len(data) <= 245):
            raise serializers.ValidationError(
                _('Errore: il campo descrizione deve avere lunghezza fra 1 e 245 caratteri.'))
        return data

    def validate_hobby(self, data):
        # controllo hobby
        if not re.match("^[A-Za-z0-9., 'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il campo hobby può contenere solo lettere, numeri, punti, virgole e spazi.'))
        if not (1 <= len(data) <= 95):
            raise serializers.ValidationError(
                _('Errore: il campo hobby deve avere lunghezza fra 1 e 95 caratteri.'))
        return data

    def validate_eta(self, data):
        # controllo eta
        if not re.match("^[0-9]+$", str(data)):
            raise serializers.ValidationError(_('Errore: l\'età può contenere solo numeri.'))
        if not (0 <= int(data) <= 100):
            raise serializers.ValidationError(_('Errore: l\'età deve essere compresa fra 0 e 100.'))
        return data


    def update(self, instance, validated_data):
        v = instance.user.username
        print(v)
        dati_utente= validated_data.pop('user')
        print("dati_utente",dati_utente)
        utente_richiedente = Profile.objects.get(user=instance.user)
        print("utente richiedente ",utente_richiedente)
        # username, first_name, last_name, email
        print("validated_data",validated_data)
        # instance.user.username = dati_utente['username']
        # instance.user.set_password(dati_utente['password'])dati_annuncio
        instance.user.first_name = dati_utente['first_name']
        instance.user.last_name = dati_utente['last_name']
        # instance.user.email = dati_utente['email']


        instance.indirizzo = validated_data['indirizzo']
        instance.citta =  validated_data['citta']
        instance.regione =  validated_data['regione']
        instance.provincia =  validated_data['provincia']
        # instance.latitudine =  validated_data['latitudine']
        # instance.longitudine =validated_data['longitudine']
        instance.telefono =validated_data['telefono']
        # instance.pet_coins =validated_data['pet_coins']
        # instance.foto_profilo =validated_data['foto_profilo']
        print("pet sitter FALSE")
        instance.pet_sitter=False
        instance.nome_pet = validated_data['nome_pet']
        instance.pet = validated_data['pet']
        instance.razza = validated_data['razza']
        instance.eta = validated_data['eta']
        instance.caratteristiche = validated_data['caratteristiche']
        # instance.foto_pet = validated_data['foto_pet']
        # instance.descrizione = validated_data['descrizione']
        # instance.hobby = validated_data['hobby']
        instance.user.save()
        instance.save()

        aggiornaLatLng(instance.user, self.context['request'])

        # latitudine, longitudine = calcola_lat_lon(self.context['request'], utente_richiedente)
        # utente_richiedente.latitudine = latitudine
        # utente_richiedente.longitudine = longitudine
        # utente_richiedente.save()

        return instance


class AnnuncioSerializer(serializers.ModelSerializer):
    data_inizio =serializers.DateTimeField(format=None, input_formats=None)
    data_fine =serializers.DateTimeField(format=None, input_formats=None)
    annuncio_valido = serializers.SerializerMethodField("get_annuncio_valido")
    user = UsernameOnlySerializer(many=False, read_only=True)
    class Meta:
        model = Annuncio
        fields = "__all__"
        read_only_fields = ("id",)

    def get_annuncio_valido(self, annuncio):
        now = datetime.datetime.now()
        if now < annuncio.data_fine:
            return True
        else:
            return False
    def validate_titolo(self, data):
        # controllo titolo
        if not re.match("^[A-Za-z0-9 .,'èòàùì]+$",data):
            raise serializers.ValidationError(
                _('Errore: il titolo può contenere solo lettere, numeri e spazi.'))
        if not (1 <= len(data) <= 95):
            raise serializers.ValidationError(
                _('Errore: il titolo deve avere lunghezza fra 1 e 95 caratteri.'))
        return data

    def validate_sottotitolo(self, data):
        # controllo sottotitolo
        if not re.match("^[A-Za-z0-9 ,.')èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il sottotitolo può contenere solo lettere, numeri, punti, virgole e spazi.'))
        if not (1 <= len(data) <= 95):
            raise serializers.ValidationError(
                _('Errore: il sottotitolo deve avere lunghezza fra 1 e 95 caratteri.'))
        return data

    def validate_descrizione(self, data):
        # controllo descrizione
        if not re.match("^[A-Za-z0-9 .,'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: la descrizione può contenere solo lettere, numeri, punti, virgole e spazi.'))
        if not (1 <= len(data) <= 245):
            raise serializers.ValidationError(
                _('Errore: il titolo deve avere lunghezza fra 1 e 245 caratteri.'))
        return data

    def validate_data_inizio(self, data):
        # controllo se data inizio < data_fine e se data_inizio e data_fine > adesso
        data_inizio = data
        if data_inizio < datetime.datetime.now():
            raise serializers.ValidationError(_('Errore: la data di inizio non può essere nel passato.'))
        return data

    def validate_data_fine(self, data):
        # controllo se data inizio < data_fine e se data_inizio e data_fine > adesso
        data_fine =data

        if data_fine < datetime.datetime.now():
            raise serializers.ValidationError(_('Errore: la data di fine non può essere nel passato.'))
        return data

    def validate_pet_coins(self, data):
        # controllo pet_coins
        if not re.match("^[0-9]+$", str(data)):
            raise serializers.ValidationError(_('Errore: il campo pet coins può contenere solo numeri.'))
        if not (1 <= int(data) <= 100000):
            raise serializers.ValidationError(
                _('Errore: il valore in pet coins deve essere compreso tra 1 e 100000.'))
        return data

    def validate_logo_annuncio(self, data):
        files = data
        if files is not None:
            file_size = files.size
            limit_MB = 5
            if file_size > limit_MB * 1024 * 1024:
                raise serializers.ValidationError("La dimensione massima per le immagini è %s MB" % limit_MB)

            file_type = magic.from_buffer(files.read(), mime=True)
            if file_type not in MIME_TYPES:
                raise serializers.ValidationError(_("file non supportato."))
            return files
        return None


class ServizioOffertoSerializer(serializers.ModelSerializer):
    # annuncio = AnnuncioSerializer(many=False)
    class Meta:
        model = Servizio
        fields = "__all__"

class AnnuncioConServizi(serializers.ModelSerializer):
    annuncio = AnnuncioSerializer(many=False)
    # annuncio_valido = serializers.SerializerMethodField("get_annuncio_valido")
    class Meta:
        model = Servizio
        fields = "__all__"

    # def get_annuncio_valido(self, servizio):
    #     now = datetime.datetime.now()
    #     if now < servizio.annuncio.data_inizio:
    #         return True
    #     else:
    #         return False

    def update(self, instance, validated_data):
        dati_annuncio = validated_data.pop('annuncio')
        instance.annuncio.titolo = dati_annuncio['titolo']
        instance.annuncio.sottotitolo = dati_annuncio['sottotitolo']
        instance.annuncio.descrizione = dati_annuncio['descrizione']
        instance.annuncio.pet = dati_annuncio['pet']
        instance.annuncio.pet_coins = dati_annuncio['pet_coins']
        instance.annuncio.data_inizio = dati_annuncio['data_inizio']
        instance.annuncio.data_fine = dati_annuncio['data_fine']
        # instance.annuncio.logo_annuncio = dati_annuncio['logo_annuncio']
        instance.annuncio.save()

        instance.passeggiate = validated_data['passeggiate']
        instance.pulizia_gabbia = validated_data['pulizia_gabbia']
        instance.ore_compagnia = validated_data['ore_compagnia']
        instance.cibo = validated_data['cibo']
        instance.accompagna_dal_vet = validated_data['accompagna_dal_vet']
        instance.save()
        return instance


    def create(self, validated_data):
        dati_annuncio = validated_data.pop('annuncio')
        # print(validated_data)
        # print(dati_annuncio)
        # request = getattr(self.context, 'request', None)
        # print(self.context)
        # print("request USER : ",self.context['request'].user)
        annuncio_nuovo=Annuncio.objects.create(user=self.context['request'].user)
        userprofile = Profile.objects.filter(user=self.context['request'].user).first()
        # print("userprofile",userprofile)
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

class ContattaciSerializer(serializers.Serializer):
    titolo = serializers.CharField(max_length=95)
    messaggio = serializers.CharField(max_length=300)

    class Meta:
        fields=['titolo', 'messaggio']

    def validate_titolo(self, data):
        if not re.match("^[A-Za-z0-9 .,'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il titolo può contenere solo lettere, numeri e spazi.'))
        if not (1 <= len(data) <= 95):
            raise serializers.ValidationError(
                _('Errore: il titolo deve avere lunghezza fra 1 e 95 caratteri.'))
        return data

    def validate_messaggio(self, data):
        if not re.match("^[A-Za-z0-9 .,'èòàùì!?]+$", data):
            raise serializers.ValidationError(
                _('Errore: il messaggio può contenere solo lettere, numeri e spazi.'))
        if not (1 <= len(data) <= 300):
            raise serializers.ValidationError(
                _('Errore: il messaggio deve avere lunghezza fra 1 e 300 caratteri.'))
        return data


class PetCoinsSerializer(serializers.Serializer):
    pet_coins = serializers.IntegerField()
    class Meta:
        fields=['pet_coins']

    def validate_pet_coins(self, data):
        # controllo descrizione
        if not re.match("^[0-9]+$", str(data)):
            raise serializers.ValidationError(_('Errore: il valore dei pet coins deve contenere solo numeri'))
        return data


class AccettaAnnuncioSerializer(serializers.Serializer):
    user_accetta = serializers.BooleanField()
    class Meta:
        fields=['user_accetta']
    def validate_user_accetta(self, data):
        # controllo descrizione
        if not re.match("^[A-Za-z]+$", str(data)):
            raise serializers.ValidationError(_('Errore: il campo può contenere solo <True> o <False>'))
        return data


class UtenteConRecensioni(serializers.ModelSerializer):
    user_recensito = DatiUtenteCompleti(many=False)
    class Meta:
        model = Recensione
        fields ="__all__"

    def validate_descrizione(self, data):
        # controllo descrizione
        if not re.match("^[A-Za-z0-9 ,.'èòàùì]+$", data):
            raise serializers.ValidationError(_('Errore: la descrizione può contenere solo lettere, '
                                    'numeri, punti, virgole e spazi.'))
        return data

    def validate_titolo(self, data):
        if not re.match("^[A-Za-z0-9 .,'èòàùì]+$", data):
            raise serializers.ValidationError(
                _('Errore: il titolo può contenere solo lettere, numeri e spazi.'))
        if not (1 <= len(data) <= 95):
            raise serializers.ValidationError(
                _('Errore: il titolo deve avere lunghezza fra 1 e 95 caratteri.'))
        return data