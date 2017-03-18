document.addEventListener("DOMContentLoaded", function(event) {
    var buttonElement = document.getElementById('runTests');
    buttonElement.onclick = function() {
        var req = new XMLHttpRequest();
        req.open('GET', window.location.protocol + '//' + window.location.host + '/demo/run');
        req.send(null);
        buttonElement.disabled = true;
    };
    buttonElement.disabled = false;
});
