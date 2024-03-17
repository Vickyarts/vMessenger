var profileStack = '';
var messageStack = {};
var profileSearch = {};
var currentChat = '';
var headsG = {};
var last_Gmessages = {};
var updatePause = false;


$(document).ready(function () {
    sendPostRequest('/data/profiles')
        .then(function (profiles) {
            profileStack = profiles;
            $('#profiles-box').empty();
            Object.keys(profiles).forEach(function (key) {
                let time = getReadableTime(profiles[key].last_time)
                $('#profiles-box').append(`<article class= "profile">
                <img class="profile-dp" src = "/asset/profileimage?id=${key}" alt = "DP" onclick="dpView(${key})" />
                <div class="profile-details" onclick="populateMessages(${key})">
                    <p class="profile-usernames">${profiles[key].display}</p>
                    <div class="profile-last-message">
                        <p class="last-message">${profiles[key].last}</p>
                        <p class="last-message-time">${time}</p>
                    </div>
                </div>
                </article>`);
            });
        });
    sendPostRequest('/data/messages')
        .then(function (stack) {
            messageStack = stack;
        });
    setTimeout(messageUpdates, 5000);
});

function messageUpdates() {
    function loop() {
        var updateStack = {};
        if (!updatePause) {
            sendPostRequest('/data/messageupdates')
                .then(function (stack) {
                    updateStack = stack;
                    insertMessageUpdates(updateStack);
                });
        }
        setTimeout(loop, 3000);
    }
    loop();
}

function insertMessageUpdates(updateStack) {
    if (updateStack != undefined) {
        Object.keys(updateStack).forEach(function (key) {
            if (messageStack.hasOwnProperty(key)) {
                Object.keys(updateStack[key]).forEach(function (subkeys) {
                    messageStack[key][subkeys] = updateStack[key][subkeys];
                });
            } else {
                messageStack[key] = {};
                Object.keys(updateStack[key]).forEach(function (subkeys) {
                    messageStack[key][subkeys] = updateStack[key][subkeys];
                });
            }
            if (key == currentChat) {
                Object.keys(updateStack[key]).forEach(function (subkeys) {
                    insertMessage(updateStack[key][subkeys]);
                });
            }
        })
    }
}


function populateMessages(id) {
    updatePause = true;
    currentChat = id;
    initiateProfileBox(id);
    $('.chat-input').css('display', 'flex');
    $('.chat-box').empty();
    let head = '';
    let last_message = '';

    Object.keys(messageStack[id.toString()]).forEach(function (key) {
        let message = messageStack[id.toString()][key];
        let time = getReadableTime(message['sent_time']);
        if (head != getReadableDate(message['sent_day'])) {
            head = getReadableDate(message['sent_day']);
            $('.chat-box').append(`
            <div class="header-time-frame">
                <div class="header-time-box">
                  <p class="header-time">${head}</p>
                </div>
            </div>
            `);
            last_message = '';
        }
        headsG[id.toString()] = head;
        if (message['action'] == 'sent') {
            if (last_message != 'sent') {
                $('.chat-box').append(`
                    <div class="sent-frame">
                    <div class="sent-box first-message sent-continues">
                    <svg
                        class="sent-tail"
                        viewBox="0 0 8 13"
                        height="13"
                        width="8"
                        preserveAspectRatio="xMidYMid meet"
                        class=""
                        version="1.1"
                        x="0px"
                        y="0px"
                        enable-background="new 0 0 8 13"
                    >
                        <title>tail-out</title>
                        <path
                        opacity="0.13"
                        d="M5.188,1H0v11.193l6.467-8.625 C7.526,2.156,6.958,1,5.188,1z"
                        ></path>
                        <path
                        fill="#1485ef"
                        d="M5.188,0H0v11.193l6.467-8.625C7.526,1.156,6.958,0,5.188,0z"
                        ></path>
                    </svg>
                    <div class="sent">
                        <p class="message white">${message["text"]}</p>
                        <div class="time-div">
                        <p class="message-time white">${time}</p>
                        </div>
                    </div>
                    </div>
                    </div>
                `);
            } else {
                $('.chat-box').append(`
                    <div class="sent-frame">
                    <div class="sent-box continues sent-continues">
                    <svg
                        class="sent-tail hide"
                        viewBox="0 0 8 13"
                        height="13"
                        width="8"
                        preserveAspectRatio="xMidYMid meet"
                        class=""
                        version="1.1"
                        x="0px"
                        y="0px"
                        enable-background="new 0 0 8 13"
                    >
                        <title>tail-out</title>
                        <path
                        opacity="0.13"
                        d="M5.188,1H0v11.193l6.467-8.625 C7.526,2.156,6.958,1,5.188,1z"
                        ></path>
                        <path
                        fill="#1485ef"
                        d="M5.188,0H0v11.193l6.467-8.625C7.526,1.156,6.958,0,5.188,0z"
                        ></path>
                    </svg>
                    <div class="sent continues-rad">
                        <p class="message white">${message["text"]}</p>
                        <div class="time-div">
                        <p class="message-time white">${time}</p>
                        </div>
                    </div>
                    </div>
                    </div>
                `);
            }
            last_message = 'sent';
        } else if (message['action'] == 'received') {
            if (last_message != 'received') {
                $('.chat-box').append(`
                    <div class="received-frame">
                    <div class="received-box first-message">
                    <svg
                        class="received-tail"
                        viewBox="0 0 8 13"
                        height="13"
                        width="8"
                        preserveAspectRatio="xMidYMid meet"
                        class=""
                        version="1.1"
                        x="0px"
                        y="0px"
                        enable-background="new 0 0 8 13"
                    >
                        <title>tail-in</title>
                        <path
                        opacity="0.13"
                        fill="white"
                        d="M1.533,3.568L8,12.193V1H2.812 C1.042,1,0.474,2.156,1.533,3.568z"
                        ></path>
                        <path
                        fill="white"
                        d="M1.533,2.568L8,11.193V0L2.812,0C1.042,0,0.474,1.156,1.533,2.568z"
                        ></path>
                    </svg>
                    <div class="received">
                        <p class="message">
                        ${message["text"]}
                        </p>
                        <div class="time-div">
                        <p class="message-time">${time}</p>
                        </div>
                    </div>
                    </div>
                    </div>
                `);
            } else {
                $('.chat-box').append(`
                <div class="received-frame">
                <div class="received-box continues">
                <svg
                    class="received-tail hide"
                    viewBox="0 0 8 13"
                    height="13"
                    width="8"
                    preserveAspectRatio="xMidYMid meet"
                    class=""
                    version="1.1"
                    x="0px"
                    y="0px"
                    enable-background="new 0 0 8 13"
                >
                    <title>tail-in</title>
                    <path
                    opacity="0.13"
                    fill="white"
                    d="M1.533,3.568L8,12.193V1H2.812 C1.042,1,0.474,2.156,1.533,3.568z"
                    ></path>
                    <path
                    fill="white"
                    d="M1.533,2.568L8,11.193V0L2.812,0C1.042,0,0.474,1.156,1.533,2.568z"
                    ></path>
                </svg>
                <div class="received continues-rad">
                    <p class="message">
                    ${message["text"]}
                    </p>
                    <div class="time-div">
                    <p class="message-time">${time}</p>
                    </div>
                </div>
                </div>
                </div>
                `);
            }
            last_message = 'received';
        }
    });
    updatePause = false;
}


$('#send-button').on("click", function () {
    if (currentChat != '') {
        let text = $('#chat-text').val();
        if (text != '') {
            let datetime = getCurrentDateandTime();
            message_data = { 'id': currentChat, 'text': text, 'time': datetime['time'], 'day': datetime['date'] };
            insertMessage({ 'action': 'sent', 'text': text, 'sent_time': datetime['time'], 'sent_day': datetime['date'] });
            let x = sendPostRequestWithData('/data/postmessage', message_data)
            $('#chat-text').val("");
        }
    }
})

$("#chat-text").keypress(function (event) {
    if (event.key == 'Enter') {
        if (currentChat != '') {
            let text = $('#chat-text').val();
            if (text != '') {
                let datetime = getCurrentDateandTime();
                message_data = { 'id': currentChat, 'text': text, 'time': datetime['time'], 'day': datetime['date'] };
                insertMessage({ 'action': 'sent', 'text': text, 'sent_time': datetime['time'], 'sent_day': datetime['date'] });
                let x = sendPostRequestWithData('/data/postmessage', message_data)
                $('#chat-text').val("");
            }
        }
    }
});

function insertMessage(message) {
    let head = headsG[currentChat];
    let time = getReadableTime(message['sent_time']);
    if (head != 'Today') {
        head = getReadableDate(message['sent_day']);
        $('.chat-box').append(`
        <div class="header-time-frame">
            <div class="header-time-box">
              <p class="header-time">${head}</p>
            </div>
        </div>
        `);
        headsG[currentChat] = head;
    }
    if (message['action'] == 'sent') {
        if (last_Gmessages[currentChat] != 'sent') {
            $('.chat-box').append(`
                <div class="sent-frame">
                <div class="sent-box first-message sent-continues">
                <svg
                    class="sent-tail"
                    viewBox="0 0 8 13"
                    height="13"
                    width="8"
                    preserveAspectRatio="xMidYMid meet"
                    class=""
                    version="1.1"
                    x="0px"
                    y="0px"
                    enable-background="new 0 0 8 13"
                >
                    <title>tail-out</title>
                    <path
                    opacity="0.13"
                    d="M5.188,1H0v11.193l6.467-8.625 C7.526,2.156,6.958,1,5.188,1z"
                    ></path>
                    <path
                    fill="#1485ef"
                    d="M5.188,0H0v11.193l6.467-8.625C7.526,1.156,6.958,0,5.188,0z"
                    ></path>
                </svg>
                <div class="sent">
                    <p class="message white">${message["text"]}</p>
                    <div class="time-div">
                    <p class="message-time white">${time}</p>
                    </div>
                </div>
                </div>
                </div>
            `);
        } else {
            $('.chat-box').append(`
                <div class="sent-frame">
                <div class="sent-box continues sent-continues">
                <svg
                    class="sent-tail hide"
                    viewBox="0 0 8 13"
                    height="13"
                    width="8"
                    preserveAspectRatio="xMidYMid meet"
                    class=""
                    version="1.1"
                    x="0px"
                    y="0px"
                    enable-background="new 0 0 8 13"
                >
                    <title>tail-out</title>
                    <path
                    opacity="0.13"
                    d="M5.188,1H0v11.193l6.467-8.625 C7.526,2.156,6.958,1,5.188,1z"
                    ></path>
                    <path
                    fill="#1485ef"
                    d="M5.188,0H0v11.193l6.467-8.625C7.526,1.156,6.958,0,5.188,0z"
                    ></path>
                </svg>
                <div class="sent continues-rad">
                    <p class="message white">${message["text"]}</p>
                    <div class="time-div">
                    <p class="message-time white">${time}</p>
                    </div>
                </div>
                </div>
                </div>
            `);
        }
        last_Gmessages[currentChat] = 'sent';
    } else if (message['action'] == 'received') {
        if (last_Gmessages[currentChat] != 'received') {
            $('.chat-box').append(`
                <div class="received-frame">
                <div class="received-box first-message">
                <svg
                    class="received-tail"
                    viewBox="0 0 8 13"
                    height="13"
                    width="8"
                    preserveAspectRatio="xMidYMid meet"
                    class=""
                    version="1.1"
                    x="0px"
                    y="0px"
                    enable-background="new 0 0 8 13"
                >
                    <title>tail-in</title>
                    <path
                    opacity="0.13"
                    fill="white"
                    d="M1.533,3.568L8,12.193V1H2.812 C1.042,1,0.474,2.156,1.533,3.568z"
                    ></path>
                    <path
                    fill="white"
                    d="M1.533,2.568L8,11.193V0L2.812,0C1.042,0,0.474,1.156,1.533,2.568z"
                    ></path>
                </svg>
                <div class="received">
                    <p class="message">
                    ${message["text"]}
                    </p>
                    <div class="time-div">
                    <p class="message-time">${time}</p>
                    </div>
                </div>
                </div>
                </div>
            `);
        } else {
            $('.chat-box').append(`
            <div class="received-frame">
            <div class="received-box continues">
            <svg
                class="received-tail hide"
                viewBox="0 0 8 13"
                height="13"
                width="8"
                preserveAspectRatio="xMidYMid meet"
                class=""
                version="1.1"
                x="0px"
                y="0px"
                enable-background="new 0 0 8 13"
            >
                <title>tail-in</title>
                <path
                opacity="0.13"
                fill="white"
                d="M1.533,3.568L8,12.193V1H2.812 C1.042,1,0.474,2.156,1.533,3.568z"
                ></path>
                <path
                fill="white"
                d="M1.533,2.568L8,11.193V0L2.812,0C1.042,0,0.474,1.156,1.533,2.568z"
                ></path>
            </svg>
            <div class="received continues-rad">
                <p class="message">
                ${message["text"]}
                </p>
                <div class="time-div">
                <p class="message-time">${time}</p>
                </div>
            </div>
            </div>
            </div>
            `);
        }
        last_Gmessages[currentChat] = 'received';
    }
}



function initiateProfileBox(id) {
    $(".individual-name").html(profileStack[id].display);
    $(".individual-profile").attr("src", "/asset/profileimage?id=" + id);
}

function dpView(id) {
    $(".profile-image").attr("src", "/asset/profileimage?id=" + id);
    $(".profile-layer").css("display", "flex");
}

$(".individual-profile").on("click", function () {
    if (currentChat != '') {
        $(".profile-image").attr("src", "/asset/profileimage?id=" + currentChat);
        $(".profile-layer").css("display", "flex");
    } else {
        $(".profile-image").attr("src", "/asset/profileimage?id=va");
        $(".profile-layer").css("display", "flex");
    }
})

$(".search-input").on("input", function () {
    let username = $(".search-input").val();
    if (username != '') {
        sendPostRequestWithData('/data/usernamesearch', { 'username': username })
            .then(function (profiles) {
                profileSearch = profiles;
                if (Object.keys(profiles).length === 0) {
                    $('.profile-finding').empty();
                    $('.profile-finding').append('<div class="profile-finding-empty"><p class="profile-finding-empty-text">No User Found!</p></div>');
                } else {
                    $('.profile-finding').empty();
                    let not_first = false;
                    Object.keys(profiles).forEach(function (keys) {
                        if (not_first) {
                            $('.profile-finding').append('<div class="profile-finding-seperation"></div>');
                        }
                        $('.profile-finding').append(`
                        <article class="profile-finding-article">
                        <img class="profile-finding-dp" src="/asset/profileimage?id=${keys}" alt="DP" />
                        <div class="profile-finding-details" onclick="addSearchedProfile(${keys})">
                            <p class="profile-finding-display">${profiles[keys].display}</p>
                            <p class="profile-finding-username">#${profiles[keys].username}</p>
                        </div>
                        </article>
                        `);
                        not_first = true;
                    });
                }
            });
    } else {
        $('.profile-finding').empty();
    }
});

function addSearchedProfile(id) {
    $('.search-frame').css('display', 'none');
    $('.profile-finding').empty();
    var newProfileStack = {};
    newProfileStack[id] = { 'username': profileSearch[id].username, 'display': profileSearch[id].display, 'last': 'Say "Hi"', 'last_time': profileSearch[id].last_time };
    $('#profiles-box').empty();
    Object.keys(profileStack).forEach(function (key) {
        newProfileStack[key] = { 'username': profileStack[key].username, 'display': profileStack[key].display, 'last': profileStack[key].last, 'last_time': profileStack[key].last_time };
    });
    Object.keys(newProfileStack).forEach(function (key) {
        let profile = newProfileStack[key];
        let time = getReadableTime(profile.last_time);
        $('#profiles-box').append(`<article class= "profile">
            <img class="profile-dp" src = "/asset/profileimage?id=${key}" alt = "DP" onclick="dpView(${key})" />
            <div class="profile-details" onclick="populateMessages(${key})">
                <p class="profile-usernames">${profile.display}</p>
                <div class="profile-last-message">
                    <p class="last-message">${profile.last}</p>
                    <p class="last-message-time">${time}</p>
                </div>
            </div>
            </article>`);
    });
    profileStack = newProfileStack;
}

var isSettingsOpen = false;
$("#menu-button").on("click", function () {
    if (!isSettingsOpen) {
        $('.settings').css('display', 'block');
        isSettingsOpen = true;
    } else {
        $('.settings').css('display', 'none');
        isSettingsOpen = false;
    }
});

$("#logout").on("click", function () {
    $(".logout-container").css("display", "flex");
    $(".logout-confimation").css("display", "block");
});

$("#logout-cancel").on("click", function () {
    $(".logout-container").css("display", "none");
    $(".logout-confimation").css("display", "none");
});

$("#logout-confirm").on("click", function () {
    sendPostRequest('/users/logout')
        .then(function (response) {
            if (response['logout'] == 200) {
                window.location.replace("/");
            }
        });
});

function sendPostRequest(url) {
    var data = {};
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

function getReadableTime(time) {
    let time_vals = time.split(":");
    let time_string = '';
    let period = '';
    const hour = parseInt(time_vals[0]);
    const minute = time_vals[1];
    console.log('before half');
    if (hour > 12) {
        period = 'PM';
        console.log(hour);
        console.log(period);
        time_string = (hour - 12).toString();
    } else {
        period = 'AM';
        time_string = hour.toString();
    }
    return time_string + ':' + minute.toString() + ' ' + period;
}

function getReadableDate(date) {
    let date_vals = date.split("-");
    let date_string = date_vals[2] + '-' + date_vals[1] + '-' + date_vals[0];
    const today = new Date();
    const day = today.getDate();
    const month = today.getMonth() + 1;
    const year = today.getFullYear();
    if (year == parseInt(date_vals[0])) {
        if (month == parseInt(date_vals[1])) {
            if (day == parseInt(date_vals[2])) {
                date_string = 'Today';
            } else if ((day - 1) == parseInt(date_vals[2])) {
                date_string = 'Yesterday';
            }
        }
    }
    return date_string;
}

function getCurrentDateandTime() {
    var currentDate = new Date();
    var currentDay = currentDate.getDate();
    var currentMonth = currentDate.getMonth() + 1;
    var currentYear = currentDate.getFullYear();
    var currentHour = currentDate.getHours();
    var currentMinute = currentDate.getMinutes();
    var currentSecond = currentDate.getSeconds();
    var date = currentYear + "-" + currentMonth + "-" + currentDay;
    var time = currentHour + ":" + currentMinute + ":" + currentSecond;
    return { 'date': date, 'time': time };
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function getAllCookies() {
    const value = `; ${document.cookie}`;
    return value;
}

$("#search-menu-button").on("click", function () {
    $('.search-frame').css('display', 'flex');
})

$("#search-cancel").on("click", function () {
    $('.search-frame').css('display', 'none');
    $('.profile-finding').empty();
})

$(".profile-image-topbar-exit").on("click", function () {
    $(".profile-layer").css('display', 'none');
})
