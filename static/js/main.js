var allClear = function() {
    var subject = document.getElementById("ticketSubject");
    var roomNum = document.getElementById("roomNumber");
    var urgency = document.getElementById("urgency");
    var nameFirst = document.getElementById("ticketGuestFirstName");
    var nameLast = document.getElementById("ticketGuestLastName");
    var email = document.getElementById("emailField");

    return subject.value && roomNum.value && nameFirst.value && nameLast.value && email.value
    
};

var notClear = (function() {

    var isClicked = false;

    return function() {
	if (!isClicked) {
	    isClicked = true;
	    $('<div id="alertMsg" class="alert alert-danger">One or more required fields were left incomplete.</div>').hide().prependTo($("#subForm")).fadeIn(500);
	}
    }
	//var msg = $('<div id="alertMsg" class="alert alert-danger">One or more required fields were left incomplete.</div>');
    /*var msg = document.createElement("div");
    msg.addClass("alert alert-warning");
    msg.innerHTML = "One or more required fields were left incomplete.";
    $("*/
    //var msg = document.getElementById("alertMsg");
    //msg.fadeIn(500);
    //$("#alertMsg").fadeIn(500);
    //document.getElementById("alertMsg").style.visibility = "";
    //document.getElementById("alertMsg").style.opacity = "1";
    /*msg.css({
	"visibility": "",
	"height": "100%",
	"opacity": "1"
	});*/

    msg.hide().prependTo($("#subForm")).fadeIn(500);
    //msg.style.display = "";
    
    /*(function() {
	msg.style.opacity = "1";
	})()*/
    
    //window.setInterval(function() {msg.style.opacity = "1";},25);
    
    //msg.style.opacity = "1";
    /*$("#alertMsg").css("opacity","1");*/
})();
