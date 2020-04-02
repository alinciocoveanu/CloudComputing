$(document).ready(function() {
    
    var submitBtn = document.getElementById("submit");

    submitBtn.addEventListener('click', function(e){
        e.preventDefault();

        var getUrl = window.location;
        var baseUrl = getUrl.protocol + "//" + getUrl.host;
        console.log(baseUrl);

        var data = {
            title: $("#title").get(0).value,
            description: $("#description").get(0).value,
            price: $("#price").get(0).value,
            duration: $("#duration").get(0).value,
            date: $("#date").get(0).value
        };
    
        var obj = JSON.stringify(data);
        console.log(obj);

        var apiCall = $.ajax(
            {
                url: baseUrl + '/api/add-advert',
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
    });
})