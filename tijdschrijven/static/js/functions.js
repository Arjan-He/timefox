$(function() {
    
    $( "#weekPicker" ).weekpicker({
    
            // set start day of the week
            firstDay: 1,
        
            // custom date format
            dateFormat: "dd/mm/yyyy",
    
            // shows other months
            showOtherMonths: true,
    
            // allows to select other months
            selectOtherMonths: true,
    
            // shows the current week number
            showWeek: true,

            // supported keywords:
            //  w  = week number, eg. 3
            //  ww = zero-padded week number, e.g. 03
            //  o  = short (week) year number, e.g. 18
            //  oo = long (week) year number, e.g. 2018
            weekFormat: "w - oo"
   
    });

    // $(".ts-urenvak").on("keypress keyup blur",function (e) {
    //     $(this).val($(this).val().replace(/[^0-9\.]/g,''));
    //        if ((e.which != 46 || $(this).val().indexOf('.') != -1) && (e.which < 48 || e.which > 57)) {
    //            e.preventDefault();
    //        }
    //  });

    $('.ts-urenvak').keypress(function(event) {
        //Allow only backspace and delete
        if (event.keyCode != 46 && event.keyCode != 8) {
            if (!parseInt(String.fromCharCode(event.which))) {
                event.preventDefault();
            }
        }
    });



});


