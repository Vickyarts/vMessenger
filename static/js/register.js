$("#username").on("input", function () {
    let username = $("#username").val();
    if (username != '') {
        sendPostRequestWithData('/users/usernamecheck', { 'username': username })
            .then(function (response) {
                if (response['username'] == '200') {
                    $(".uname-available").css("display", "block");
                    $(".uname-not-available").css("display", "none");
                } else {
                    $(".uname-available").css("display", "none");
                    $(".uname-not-available").css("display", "block");
                }
            });
    } else {
        $(".uname-available").css("display", "none");
        $(".uname-not-available").css("display", "none");
    }
});



function sendPostRequestWithData(url, data) {
    const csrfToken = getCookie('csrftoken');
    const xkey = getCookie('x-key');
    data['csrfmiddlewaretoken'] = csrfToken;
    data['x-key'] = xkey;
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

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}