$.validator.methods.email = function( value, element ) {
  return this.optional( element ) || /[a-z]+@[a-z]+\.[a-z]+/.test( value );
}

jQuery.validator.setDefaults({
  success: 'valid'
});

jQuery.validator.addMethod("lettersonly", function(value, element) {
  return this.optional(element) || /^[a-z]+$/i.test(value);
}, "Caratteri numerici non ammessi");

jQuery.validator.addMethod("username_unique", function(value, element) {

    var isSuccess = false;

   $.ajax({ url: "/utenti/check_username",
            type: "GET",
            data: "username=" + value,
            async: false,
            dataType:"html",
            success: function(msg) { isSuccess = msg === "True" }
          });
    return isSuccess;
}, "Username non disponibile");

jQuery.validator.addMethod("eta_pet_valida", function(value, element) {
  return value >= 0 && value <= 100;
}, "L'età deve essere compresa tra 0 e 100 anni");

$( '#user-form' ).validate({
  rules: {
    'username':{
        required: true,
        minlength: 3,
        username_unique: true
        },
    'email':{
        required: true,
        email: true
        },
    'password':{
        required: true,
        minlength: 4
        },
    'conferma_password':{
        equalTo: '#password'
        },
      'first_name': {
        required: true,
        lettersonly: true
      },
      'last_name':{
        required: true,
        lettersonly: true
      },
      'indirizzo': {
        required: true
      },
      'citta':{
        required: true,
        lettersonly: true
      },
      'telefono':{
        required: true,
        number: true
      },
      'eta':{
        required: true,
        number: true,
        eta_pet_valida: true
      },
      'nome_pet':{
        required: true,
        lettersonly: true
      },
      'razza':{
        required: true,
        lettersonly: true
      },
      'caratteristiche':{
        required: true
      }
  },
  messages:
    {
    'username':{
        required: "Il campo username è obbligatorio",
        minlength: "Scegli un username di almeno 3 lettere"
        },
    'email':{
        required: "Il campo email è obbligatorio",
        email: "Inserisci un valido indirizzo email"
        },
    'password':{
        required: "Il campo password è obbligatorio",
        minlength: "Inserisci una password di almeno 4 caratteri"
        },
    'conferma_password':{
        equalTo: "Le due password non coincidono"
        },
    'first_name': {
        required: "Il campo nome è obbligatorio",
        notNumber: "Caratteri numerici non consentiti"
      },
    'last_name':{
        required: "Il campo cognome è obbligatorio"
      },
    'indirizzo': {
        required: "Il campo indirizzo è obbligatorio"
      },
    'citta':{
        required: "Il campo citta è obbligatorio"
     },
    'telefono':{
        required: "Il campo telefono è obbligatorio",
        number: "Inserisci un numero valido"
     },
     'eta':{
        required: "Il campo età è obbligatorio",
        number: "Inserisci un numero valido"
     },
     'nome_pet':{
        required: "Il campo nome pet è obbligatorio"
      },
    'razza': {
        required: "Il campo razza è obbligatorio"
      },
    'caratteristiche':{
        required: "Il campo caratteristiche è obbligatorio"
     }
    }
});
