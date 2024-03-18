

function isEmail(text) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(text);
}

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



$('#forgot-btn').click(function () {
    mail = $('#email').val();
    if (isEmail(mail)) {
        data = { 'email': mail };
        let x = sendPostRequestWithData('/users/forgot', data);
        $('.forgot-sent-box').css('display', 'flex');
        $('.forgot-box').css('display', 'none');
    }
});