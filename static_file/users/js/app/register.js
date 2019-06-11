// ajax发送注册表单
$(function () {
    $("#submit").click(function () {
        var token = $('input[name=csrfmiddlewaretoken]').val();
        email = $("#email").val();
        password = $("#password").val();
        confirm_password = $("#confirm_password").val();
        // console.log(email, password, confirm_password);
        form_list = {csrfmiddlewaretoken: token};
        form_list['email'] = email;
        form_list['password'] = password;
        form_list['confirm_password'] = confirm_password;
        // console.log(form_list);
        $.ajax({
            url: "/users/api/v1/ajax_reg/",
            method: "POST",
            dataType: "json",
            data: form_list,
            success:function (data) {
                console.log(data);
                if (data.code == 0){
                // window.location.href="/users/";
                    $("#msg").html("<span style='color:green;'>" + data.msg + "</span>")
                    setTimeout("javascript:location.href='/users/'", 2000);
                }else{
                    $("#msg").html("<span style='color:red;'>" + data.msg + "</span>")
                }
            }
        })
    })
});