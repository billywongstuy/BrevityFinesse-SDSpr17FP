var allClear = function() {
    var subject = document.getElementById("ticketSubject");
    var roomNum = document.getElementById("roomNumber");
    var urgency = document.getElementById("urgency");
    var nameFirst = document.getElementById("ticketGuestFirstName");
    var nameLast = document.getElementById("ticketGuestLastName");
    var email = document.getElementById("emailField");

    return subject.value && roomNum.value && nameFirst.value && nameLast.value && email.value
    
};

var notClear = function() {
    /*var msg = document.createElement("div");
    msg.addClass("alert alert-warning");
    msg.innerHTML = "One or more required fields were left incomplete.";
    $("*/
    document.getElementById("alertMsg").style.display = "";
    /*document.getElementById("alertMsg").style.opacity = "1";*/
    $("#alertMsg").css("style","1");
};
