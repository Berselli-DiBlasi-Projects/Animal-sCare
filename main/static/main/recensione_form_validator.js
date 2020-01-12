jQuery.validator.setDefaults({
  success: "valid"
});

$( "#recensione-form" ).validate({
  rules: {
      'titolo':{
        required: true
      },
      'descrizione':{
        required: true
      }
  },
  messages:
    {
        'titolo':{
        required: "Il campo titolo è obbligatorio"
      },
      'descrizione':{
        required: "Il campo descrizione è obbligatorio"
      }
    }
});