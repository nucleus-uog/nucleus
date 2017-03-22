document.addEventListener("DOMContentLoaded", function(event) {
    var intervalId;
    updateStatus = function() {
        // Gets the badge of tests currently running
        var elements = document.getElementsByClassName('status-check');
        if(elements.length < 1) clearInterval(intervalId);

        // Updates the status of the tests automatically 
        for (var i = 0; i < elements.length; i++) {
            var el = elements[i];
            var id = el.id;
            id = id.replace('status-', '');

            var req = new XMLHttpRequest();
            req.open('GET', window.location.protocol + '//' + window.location.host + '/status/'+id);
            req.send(null);
            req.onreadystatechange = changeStatus;
        }
    }
    updateStatus();
    intervalId = setInterval(updateStatus, 5000);
});

function changeStatus(){
  if(this.readyState == 4 && this.status == 200){
    var data = JSON.parse(this.responseText);
    var el = document.getElementById('status-'+data['id']);
    el.className = data['class'];

    // Updates status badge if the status of the tests has changed
    var inner = '<i class="' + data['icon'].replace("\"", '') + '"></i> ' + data['status'];
    if(el.innerHTML != inner) el.innerHTML = inner;

    // Reloads the page if a test has complete
    if(!data['class'].includes("status-check")) location.reload();
  }
}
