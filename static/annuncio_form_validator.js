jQuery.validator.setDefaults({
  success: "valid"
});

var data_control = false;

jQuery.validator.addMethod("validDate", function(value, element) {
    return this.optional(element) || moment(value,"DD/MM/YYYY HH:mm").isValid();
}, "Inserisci una data valida nel formato \"DD/MM/YYYY HH:mm\"");

jQuery.validator.addMethod("notInThePast", function(value, element) {
    return this.optional(element) || moment(value,"DD/MM/YYYY HH:mm") > moment();
}, "La data non può essere nel passato");

jQuery.validator.addMethod("lowerThanDataFine", function(value, element, param) {
    if(data_control) {
        data_control = false;
        $('#id_data_fine').valid();
    }
    else
        data_control = true;
    return this.optional(element) || moment(value,"DD/MM/YYYY HH:mm") < moment($(param).val(), "DD/MM/YYYY HH:mm");
}, "Data di inizio deve essere minore della data di fine");

jQuery.validator.addMethod("greaterThanDataInizio", function(value, element, param) {
    if(data_control) {
        data_control = false;
        $('#id_data_inizio').valid();
    }
    else
        data_control = true;
    return this.optional(element) || moment(value,"DD/MM/YYYY HH:mm") > moment($(param).val(), "DD/MM/YYYY HH:mm");
}, "Data di fine deve essere maggiore della data di inizio");

$.validator.addMethod('lowStrict', function (value, el, param) {
    return value < param;
});

$( "#annuncio-form" ).validate({
  rules: {
      'titolo':{
        required: true,
        maxlength: 95
      },
      'sottotitolo': {
        required: true,
        maxlength: 95
      },
      'descrizione':{
        required: true,
        maxlength: 245
      },
      'pet_coins':{
        required: true,
        number: true,
        lowStrict: 100001
      },
      'data_inizio': {
        required: true,
        validDate: true,
        notInThePast: true,
        lowerThanDataFine: '#id_data_fine'
      },
      'data_fine': {
        required: true,
        validDate: true,
        notInThePast: true,
        greaterThanDataInizio: '#id_data_inizio'
      }
  },
  messages:
    {
        'titolo':{
        required: "Il campo titolo è obbligatorio",
        maxlength: "Limite di 95 caratteri superato"
      },
      'sottotitolo': {
        required: "Il campo sottotitolo è obbligatorio",
        maxlength: "Limite di 95 caratteri superato"
      },
      'descrizione':{
        required: "Il campo descrizione è obbligatorio",
        maxlength: "Limite di 245 caratteri superato"
      },
      'pet_coins':{
        required: "Il campo pet coins è obbligatorio",
        number: "Inserire un numero valido",
        lowStrict: "Limite di 100000 pet coins superato"
      }
    }
});
