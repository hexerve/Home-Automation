$(function () {
    $('#reset_btn').click(function () {
        if (getCookie("pass_token") === "") {
            window.location.href = "/login?action=login_required";
        } else {
            let new_pass = $("#pass").val();
            if(isText(new_pass)) {
            $('.alert').hide(500);
            $('#pass-msg').append(
                '<div class="alert alert-danger alert-dismissible fade show">' +
                '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                '<strong>Oops! </strong>Password must be 8 character long' +
                '</div>'
            );
        }
            if (new_pass !== $("#conf_pass").val()) {
                alert("new password and confirm password does not match");
                return;
            }

            let data = {};
            data.newPassword = new_pass;
            $.ajaxSetup({
                headers: {
                    'authorization': getCookie("pass_token")
                }
            });
            $.ajax({
                url: "/password/set",
                type: 'PUT',
                data: JSON.stringify(data),
                contentType: 'application/json',
                success: function (data) {
                    $('.alert').hide(500);
                    $('#pass-msg').append(
                        '<div class="alert alert-success alert-dismissible fade show">' +
                        '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                        '<strong>Congratulation! </strong>Password successfully updated</div>'
                    );
                    setTimeout(function(){
                        window.location.href = "/login";
                    }, 1000);
                },
                error: function (xhr, textStatus, errorThrown) {
                    var errMsg;

                    if (xhr.status === 0) {
                        errMsg = "Network error.";
                    } else {
                        errMsg = JSON.parse(xhr.responseText).message;
                        errMsg = errMsg.charAt(0).toUpperCase() + errMsg.substr(1);
                        if (errMsg === 'Validation failed.') {
                            errMsg += '<br/>Incorrect ' + JSON.parse(xhr.responseText).errors.index.join(", ");
                        }
                    }

                    $('.alert').hide(500);
                    $('#pass-msg').append(
                        '<div class="alert alert-danger alert-dismissible fade show">' +
                        '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                        '<strong>Oops! </strong>' + errMsg +
                        '</div>'
                    );
                }
            });
        }
    });

    showBody();

});