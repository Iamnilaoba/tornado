$(function () {
    $("#send_sms_code_btn").click(function (ev) {
        ev.preventDefault();
        $.ajax({
            url:"/sen_code/",
            type:"post",
            data:{
              "telephone" :$("#telephone").val(),
            },
            success:function (data) {
                var j = jQuery.parseJSON(data)
                if(j.code == 200 ){
                    xtalert.alertSuccessToast(j.msg)
                    var timer;
                    var num = 60;
                    $('#send_sms_code_btn').attr("disabled",true);
                    clearInterval(timer);
                    timer = setInterval(function () {
                        num--;
                        if (num<=0){
                            clearInterval(timer);
                            $('#send_sms_code_btn').attr("disabled",false);
                            $("#send_sms_code_btn").html("重新发送")
                        }else {
                            $("#send_sms_code_btn").html(num+"s后重新发送")
                        }
                    },1000)
                }else {
                    xtalert.alertErrorToast(j.msg)
                }
            }
        })
    });
    $("#signin_btn").click(function (ev) {
        ev.preventDefault();
        $.ajax({
            url:"/findpwd/",
            type:"post",
            data:{
                "telephone":$("#telephone").val(),
                "smscode":$("#smscode").val(),
                "password":$("#password").val(),
                "password1":$("#password1").val(),
            },
            success:function (data) {
                var j = jQuery.parseJSON(data)
                if(j.code == 200){
                    xtalert.alertSuccessToast(j.msg);
                    window.location = "/";
                }else {
                    xtalert.alertErrorToast(j.msg)
                }
            }
        })
    })

});
