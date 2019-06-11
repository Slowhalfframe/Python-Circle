// ajax发送登录表单
$(function () {
    $("#sign_in").click(function () {
        var token = $('input[name=csrfmiddlewaretoken]').val();
        email = $("#email").val();
        password = $("#password").val();
        next_url = $("#next").val();
        // if (next is not None)
        if($('#islong').is(':checked')) {
            islong = "on"
        }
        else{
            islong = ""
        }
        console.log(email, password, next_url);
        form_list = {csrfmiddlewaretoken: token};
        form_list['email'] = email;
        form_list['password'] = password;
        form_list['islong'] = islong;
        form_list['next_url'] = next_url
        console.log(form_list);
        $.ajax({
            url: "/users/api/v1/ajax_sign_in/",
            method: "POST",
            dataType: "json",
            data: form_list,
            success:function (data) {
                console.log(data)
                if (data.code == 0){
                // window.location.href="/users/";
                    $("#msg").html("<span style='color:green;'>" + data.msg + "</span>")
                    setTimeout("javascript:location.href=next_url", 2000);
                }else{
                    $("#msg").html("<span style='color:red;'>" + data.msg + "</span>")
                }
            }
        })
    })
});