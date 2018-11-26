$(function () {
    $('#admin').hide();
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

                // let name = data.results.user.name;

                // name = name.charAt(0).toUpperCase() + name.substr(1);

                // $(".username").text(name);

                // currentUserID =  _id;
                if (data.results.user.isAdmin) {
                    $('#admin').show();
                }

                if (data.results.devices) {
                    data.results.devices.forEach(device => {
                        $('#devices').append(
                            '<div class="card">' +
                            '<div class="card-header" id="heading_' + device.deviceId + '">' +
                            '<h5 class="mb-0">' +
                            '<div class="btn btn-block text-dark font-weight-bold" data-toggle="collapse" data-target="#collapse_' + device.deviceId + '" aria-expanded="true" aria-controls="collapse_' + device.deviceId + '">' +
                            device.name +
                            '</div>' +
                            '</h5>' +
                            '</div>' +

                            '<div id="collapse_' + device.deviceId + '" class="collapse show" aria-labelledby="heading_' + device.deviceId + '" data-parent="#accordion">' +
                            '<div class="card-body text-dark">' +
                            '<div>' +
                            '1: <input id="switch-' + device.deviceId + '-0" class="switch" type="checkbox"' + (device.values["0"] ? 'checked' : '') + '/><br/>' +
                            '2: <input id="switch-' + device.deviceId + '-1" class="switch" type="checkbox"' + (device.values["1"] ? 'checked' : '') + ' /><br/>' +
                            '3: <input id="switch-' + device.deviceId + '-2" class="switch" type="checkbox"' + (device.values["2"] ? 'checked' : '') + ' /><br/>' +
                            '4: <input id="switch-' + device.deviceId + '-3" class="switch" type="checkbox"' + (device.values["3"] ? 'checked' : '') + ' /><br/>' +
                            '5: <input id="switch-' + device.deviceId + '-4" class="switch" type="checkbox"' + (device.values["4"] ? 'checked' : '') + ' /><br/>' +
                            '</div>' +
                            '</div>' +
                            '</div>' +
                            '</div>'
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


    $(document).on('click', '.switch', function (e) {
        let data = {};

        data.deviceId = $(e.currentTarget).attr('id').split('-')[1];
        data.id = $(e.currentTarget).attr('id').split('-')[2];
        val = document.getElementById($(e.currentTarget).attr('id')).checked;

        if (val) {
            data.val = 'ON';
        } else {
            data.val = 'OFF';
        }

        $.ajax({
            url: "../operate",
            type: 'PUT',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function (result) {

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