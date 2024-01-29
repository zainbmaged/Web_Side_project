


$(document).ready(function(){
    $('.hidden').on('click', function(){
        if ($('.hidden').text()=='<<'){
                    $('.hidden').css('left', '0px');
                    $('.hidden').text('>>');
                    $('.filter').hide();

        }
        else{
            $('.hidden').css('left', '12vw');
            $('.hidden').text('<<');
            $('.filter').show();


        }            

    })
}
)
