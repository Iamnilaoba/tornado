$(function () {
    $("#changepwd").click(function (ev) {
        ev.preventDefault();
        oldpwd=$('#oldpwd').val();
        newpwd=$('#newpwd').val();
        newpwd1=$('#newpwd1').val();
        csrf = $('meta[name=csrf_token]').attr("value");
        $.ajax({
            url:'/cms/changepwd/',
            type:'post',
            data:{
                "oldpwd":oldpwd,
                'newpwd':newpwd,
                'newpwd1':newpwd1,
            },
            success:function (data) {
                var obj=jQuery.parse(data);
                if (obj.code==200){
                    xtalert.alertSuccessToast("修改密码成功")
                    $('#oldpwd').val('');
                    $('#newpwd').val('');
                    $('#newpwd1').val('');

                }else{
                    xtalert.alertErrorToast(obj.msg)
                }
            }
        })
    })
})
