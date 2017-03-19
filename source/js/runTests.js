document.addEventListener("DOMContentLoaded", function(event) {
    var intervalId;
    updateStatus = function() {
        var elements = document.getElementsByClassName('status-check');
        if(elements.length < 1) clearInterval(intervalId);
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
    el.innerHTML = data['status'];
  }
}
