$(function () {
    $("#sendemailcode").click(function (ev) {
        ev.preventDefault();
        countdown=$(this);
        email=$("#newemail").val();
        $.ajax({
            url:'/cms/send_email_code/',
            type:'post',
            data:{
                'email':email
            },
            success:function (data) {
                var obj=jQuery.parseJSON(data)
                if (obj.code==200){
                    xtalert.alertSuccessToast(obj.msg);
                            countdown.attr('disabled', true);
                            var time=60;
                            countdown.html(time+'s');
                            timer=setInterval(function () {
                            countdown.html(--time+'s');
                                if (time<=0){
                                clearInterval(timer);
                                countdown.html('再次发送');
                                countdown.attr('disabled', false)
                        }
                    },1000)

                }else {
                    xtalert.alertErrorToast(obj.msg)
                }
            }
        })
    })
});
$(function () {
    $('#changeemail').click(function (ev) {
        ev.preventDefault();
        email=$("#newemail").val();
        emailcode=$('#newemailcode').val();
        $.ajax({
            url:'/cms/changeemail/',
            type:'post',
            data:{
                'email':email,
                'emailcode':emailcode,
            },
            success:function (data) {
                var obj=jQuery.parseJSON(data)
                if (obj.code==200){
                    xtalert.alertSuccessToast('修改邮箱成功')
                }else {
                    xtalert.alertErrorToast(obj.msg)
                }
            }
        })
    })
})