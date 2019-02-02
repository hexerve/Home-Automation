var userID;
$(function () {
    if (getCookie("token") === "") {
        window.location.href = "/";
    } else {
        $.ajaxSetup({
            headers: {
                'authorization': getCookie("token")
            }
        });
        $.get("../user", {},
            function (data, status, xhr) {
                console.log(data);
                userID = data.results.user._id;
                // let name = data.results.user.name;

                // name = name.charAt(0).toUpperCase() + name.substr(1);

                // $(".username").text(name);

                // currentUserID = data.results.user._id;
                if (data.results.user.isAdmin) {
                    $('#admin').show();
                }

                if (data.results.devices) {
                    data.results.devices.forEach(device => {
                        $('#deviceList').append(
                            '<tr id="list_' + device.deviceId + '">' +
                            '<td> <input type="text" id="device_' + device.deviceId + '" class="form-control" placeholder="name" value="' + device.name + '" ></input></td>' +
                            '<td> <input type="button" class="form-control btn-light update" id="update_' + device.deviceId + '" class="text-light" value="Update"></input></td>' +
                            '<td> <input type="button" class="form-control btn-light remove" id="remove_' + device.deviceId + '" class="text-light" value="Remove"></input></td>' +
                            '</tr>'
                        );
                    });
                }

                showBody();
            }).fail(function (xhr, status, error) {
                if (xhr.status === 0) {
                    $('.alert').hide(500);
                    $('#err').append(
                        '<div class="alert alert-danger alert-dismissible fade show">' +
                        '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                        '<strong>Oops! </strong>Network error.</div>'
                    );
                    showBody();
                    return;
                }

                setCookie("token", "", -1);
                showBody();
            });
    }


    $(document).on('click', '.update', function (e) {
        let deviceId = $(e.currentTarget).attr('id').split('_')[1]
        let deviceName = $('#device_' + deviceId).val()
        if (deviceId == "" || deviceName == "") {
            $('.alert').hide(500);
            $('#err').append(
                '<div class="alert alert-danger alert-dismissible fade show">' +
                '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                '<strong>Oops! </strong>Please input the name.' +
                '</div>'
            );
            return;
        }

        let data = {
            "deviceId": deviceId,
            "deviceName": deviceName,
        };
        $.ajax({
            url: "../devices",
            type: 'PUT',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function (result) {
                $('.alert').hide(500);
                $('#err').append(
                    '<div class="alert alert-success alert-dismissible fade show">' +
                    '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                    '<strong>Congratulations! </strong> Device updated successfully' +
                    '</div>'
                );
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
                $('#err').append(
                    '<div class="alert alert-danger alert-dismissible fade show">' +
                    '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                    '<strong>Oops! </strong> ' + errMsg +
                    '</div>'
                );
            }
        });
    });

    $(document).on('click', '.remove', function (e) {
        let deviceId = $(e.currentTarget).attr('id').split('_')[1]

        let data = {
            "deviceId": deviceId,
        };
        $.ajax({
            url: "../devices",
            type: 'DELETE',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function (result) {
                $('.alert').hide(500);
                $('#err').append(
                    '<div class="alert alert-success alert-dismissible fade show">' +
                    '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                    '<strong>Congratulations! </strong> Device removed successfully' +
                    '</div>'
                );
                $('#list_' + deviceId).hide()
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
                $('#err').append(
                    '<div class="alert alert-danger alert-dismissible fade show">' +
                    '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                    '<strong>Oops! </strong> ' + errMsg +
                    '</div>'
                );
            }
        });
    });

    $(document).on('click', '#submit', function () {
        let SSID = $('#SSID').val();
        let pass = $('#pass').val();

        if (SSID == "" || pass == "") {
            $('.alert').hide(500);
            $('#err').append(
                '<div class="alert alert-danger alert-dismissible fade show">' +
                '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                '<strong>Oops! </strong>SSID or password missing.' +
                '</div>'
            );
            return;
        }

        let data = {
            "ssid": SSID,
            "password": pass,
        };
        $.ajax({
            url: "http://192.168.4.1",
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function (result) {
                let data = {
                    "deviceId": result
                };
                $.ajax({
                    url: "../devices",
                    type: 'POST',
                    data: JSON.stringify(data),
                    contentType: 'application/json',
                    success: function (result) {
                        console.log(result)
                        alert("done");
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
                        $('#err').append(
                            '<div class="alert alert-danger alert-dismissible fade show">' +
                            '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                            '<strong>Oops! </strong> ' + errMsg +
                            '</div>'
                        );
                    }
                });
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
                $('#err').append(
                    '<div class="alert alert-danger alert-dismissible fade show">' +
                    '<button type="button" class="close" data-dismiss="alert">&times;</button>' +
                    '<strong>Oops! </strong> ' + errMsg +
                    '</div>'
                );
            }
        });
    });
});