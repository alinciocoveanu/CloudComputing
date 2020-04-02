$(document).ready(function () {
    
    const button = document.getElementById("google-button");

    var getUrl = window.location;
    var baseUrl = getUrl.protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[1];

    button.addEventListener('click', function (e) {
        request(baseUrl + 'login', 'GET')
            .done(() => {
                window.location.replace(baseUrl + 'index')
            });
    });
}); 