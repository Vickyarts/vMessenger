


function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function sendPostRequestWithData(url, data) {
    const csrfToken = getCookie('csrftoken');
    data['csrfmiddlewaretoken'] = csrfToken;
    return new Promise(function (resolve, reject) {
        $.ajax({
            url: url,
            type: 'POST',
            xhrFields: {
                withCredentials: false
            },
            data: data,
            success: function (response) {
                /*console.log(response);*/
                resolve(JSON.parse(response));

            },
            error: function (xhr, status, error) {
                console.error(xhr.responseText);
                reject(xhr.responseText);
            }
        });
    });
}



$('#reset-btn').click(function () {
    pass = $('#pass').val();
    conpass = $('#conpass').val();
    if (pass === conpass) {
        console.log(pass);
        data = { 'pass': pass };
        /*let x = sendPostRequestWithData('/users/passreset', data);*/
        $('.forgot-sent-box').css('display', 'flex');
        $('.forgot-box').css('display', 'none');
    }
});

$('#pass').on("change", function () {
    pass = $('#pass').val();
    if (pass.length >= 8) {
        $('.pass-req-box').css('display', 'none')
    } else {
        $('.pass-req-box').css('display', 'block')
    }
});

$('#conpass').on("change", function () {
    pass = $('#pass').val();
    conpass = $('#conpass').val();
    if (pass === conpass) {
        $('.pass-match-box').css('display', 'none')
    } else {
        $('.pass-match-box').css('display', 'block')
    }
});