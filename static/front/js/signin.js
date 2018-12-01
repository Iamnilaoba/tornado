$(function () {
    $('#signin_btn').click(function (ev) {
        telephone=$('input[name=telephone]').val();
        password=$('input[name=password]').val();
        ev.preventDefault();
        $.ajax({
            url:'/sinin/',
            type:'post',
            data:{
                'telephone':telephone,
                'password':password
            },
            success:function (data) {
                var j = jQuery.parseJSON(data)
                if(j==200){
                    xtalert.alertSuccessToast(j.msg);
                    window.location = "/";
                }else {
                    xtalert.alertErrorToast(j.msg)
                }
            }
        })
    })
});




