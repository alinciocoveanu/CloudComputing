$(document).ready(function () {
    var getUrl = window.location;
    var baseUrl = getUrl.protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[1];
    
    const button = document.getElementById("addButton");

    button.addEventListener('click', function () {
        window.location.replace(baseUrl + "display-advert");
    });
}); 

function setCalendarEvent(advertId) {
    var getUrl = window.location;
    var baseUrl = getUrl.protocol + "//" + getUrl.host + "/" + getUrl.pathname.split('/')[1];
    console.log(advertId);

    data = {
        advertId: advertId
    };
    obj = JSON.stringify(data);

    var apiCall = $.ajax(
        {
            url: baseUrl + 'api/add-event',
            data: obj,
            contentType: "application/json",
            method: 'POST'
        }
    );

    apiCall.done(() => {
        window.location.replace(baseUrl);
    });

    apiCall.fail((e) => {
        console.log(e)
    });

}