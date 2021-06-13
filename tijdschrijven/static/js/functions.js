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

    $('.ts-urenvak').on('change',function(){

        let dag = $(this).attr('daginweek');
        dagtotaal(dag);
        let abonnment = $(this).attr('abonnementdag');
        abonnementtotaal(abonnment);
        eindtotaal();

    })

/*     $('#tijdgrid').DataTable({
        "lengthMenu": [[-1], ["All"]],
        "lengthChange": false,
        "order": [],
        "bFilter": false,
        "bPaginate": false,
        "info": false,
    }); */

    if($('#tijdgrid').length){
        
        for(let i=0;i<8;i++){dagtotaal(i);}

        $('.ts-abonnementtotaal').each(function(){
            abonnementtotaal($(this).attr('abonnement'));
        });

        eindtotaal();

    }

});

function abonnementtotaal(abonnement){
    let som = 0;
    $('input[abonnementdag="'+abonnement+'"]').each(function() {
        som += $(this).val() * 1;
    });
    $('input[abonnement="'+abonnement+'"]').val(som);
}


function dagtotaal(dag){
    
    let som = 0;
    $('input[dagnummer="'+dag+'"]').each(function() {
        som += $(this).val() * 1;
    });
    $('input[weekdag="'+dag+'"]').val(som);

}

function eindtotaal(){
    let som = 0;
    $('.ts-dagtotaal').each(function(){
        som += $(this).val() * 1;
    });
    $("#ts-eindtotaal").val(som);
}


