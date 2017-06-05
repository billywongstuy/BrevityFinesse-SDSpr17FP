var allClear = function() {
    var subject = document.getElementById("ticketSubject");
    var roomNum = document.getElementById("roomNumber");
    var urgency = document.getElementById("urgency");
    var nameFirst = document.getElementById("ticketGuestFirstName");
    var nameLast = document.getElementById("ticketGuestLastName");
    var email = document.getElementById("emailField");

    return subject.value && roomNum.value && nameFirst.value && nameLast.value //&& email.value
    
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
