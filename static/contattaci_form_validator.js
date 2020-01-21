jQuery.validator.setDefaults({
  success: "valid"
});

$( "#contattaci-form" ).validate({
  rules: {
      'titolo':{
        required: true,
        maxlength: 50
      },
      'messaggio':{
        required: true,
        maxlength: 250
      }
  },
  messages:
    {
        'titolo':{
        required: "Il campo titolo è obbligatorio",
        maxlength: "Limite di 50 caratteri superato"
      },
      'messaggio':{
        required: "Il campo messaggio è obbligatorio",
        maxlength: "Limite di 250 caratteri superato"
      }
    }
});