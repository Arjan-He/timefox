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

});


