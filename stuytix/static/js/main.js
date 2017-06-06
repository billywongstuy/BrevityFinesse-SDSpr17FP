var allClear = function() {
    var fields = {
	subject: document.getElementById("ticketSubject"),
	roomNum: document.getElementById("roomNumber"),
	//urgency: document.getElementById("urgency"),
	nameFirst: document.getElementById("ticketGuestFirstName"),
	nameLast: document.getElementById("ticketGuestLastName"),
	//email: document.getElementById("emailField")
    };
    /*var subject = document.getElementById("ticketSubject");
    var roomNum = document.getElementById("roomNumber");
    var urgency = document.getElementById("urgency");
    var nameFirst = document.getElementById("ticketGuestFirstName");
    var nameLast = document.getElementById("ticketGuestLastName");
    var email = document.getElementById("emailField");*/

    var clear = true;
    
    for (field in fields) {
	console.log(fields[field]);
	if (!fields[field].value) {
	    $(fields[field]).parent().addClass("has-error");
	    clear = false;
	}
    }

    //return subject.value && roomNum.value && nameFirst.value && nameLast.value //&& email.value
    return clear;
    
};

var notClear = (function() {
    var isClicked = false;
    return function() {
	if (!isClicked) {
	    isClicked = true;
	    $('<div id="alertMsg" class="alert alert-danger">One or more required fields were left incomplete.</div>').hide().prependTo($("#subForm")).fadeIn(500);
	}
    }
})();
