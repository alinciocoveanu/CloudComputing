const callApi = async (url) => {
    const res = await fetch(url);
    return await res.json()
};


document.getElementById("myBtn").addEventListener("click", async function() {
    let response = await callApi('http://127.0.0.1:5000/getJoke/');
    console.log(response);

    document.getElementById('jokeImg').style.backgroundImage = `url('${response['URL']}')`;
    document.getElementById('header1').innerText = response['ENTITY'];
    document.getElementById('para1').innerText = response['JOKE'];
});


window.addEventListener("load", async function() {
    let response = await callApi('http://127.0.0.1:5000/getMetrics/');
    console.log(response);

    document.getElementById('latency').innerText = response['LATENCY'] + " seconds";
    document.getElementById('successRate').innerText =  response['SUCCESS_RATE'];
    document.getElementById('totalRequests').innerText =  response['TOTAL_REQUESTS'];
    document.getElementById('successfulRequests').innerText =  response['SUCCESSFUL_REQUESTS'];
});
