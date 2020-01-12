jQuery.validator.setDefaults({
  success: "valid"
});

$( "#annuncio-form" ).validate({
  rules: {
      'titolo':{
        required: true
      },
      'sottotitolo': {
        required: true
      },
      'descrizione':{
        required: true
      },
      'pet_coins':{
        required: true,
        number: true
      }
  },
  messages:
    {
        'titolo':{
        required: "Il campo titolo è obbligatorio"
      },
      'sottotitolo': {
        required: "Il campo sottotitolo è obbligatorio"
      },
      'descrizione':{
        required: "Il campo descrizione è obbligatorio"
      },
      'pet_coins':{
        required: "Il campo pet coins è obbligatorio",
        number: "Inserire un numero valido"
      }
    }
});
