let participants = [
    {
        Name: "Ali",
        regNo: 101,
        dept: "CS",
        ticketType: "child",
        paymentStatus: "paid",
        attendanceStatus: "p"
    },

    {
        Name: "Ahmed",
        regNo: 102,
        dept: "SE",
        ticketType: "adult",
        paymentStatus: "paid",
        attendanceStatus: "a"
    },

    {
        Name: "Aliaa",
        regNo: 103,
        dept: "CS",
        ticketType: "senior",
        paymentStatus: "not paid",
        attendanceStatus: "p"
    }
];


// 1. Display Participant Details

function displayParticipants() {
    participants.forEach(function (d) {
        console.log(
            d.Name +
            " with regno " + d.regNo +
            " having type as " + d.ticketType +
            " has payment status as " + d.paymentStatus
        );
    });
}

displayParticipants();


// 2. Find Participant

function findParticipant(findd) {
    let found = participants.find(function (v) {
        return v.regNo === findd;
    });

    return found;
}

console.log(findParticipant(101));


// 3. Get Unpaid Participants

function findUnpaid() {
    let found = participants.filter(function (v) {
        return v.paymentStatus === "not paid";
    });

    return found;
}

console.log(findUnpaid());


// 4. Mark Attendance

function markAttendance(regNo) {

    let found = participants.find(function (v) {
        return v.regNo === regNo;
    });

    if (found) {
        found.attendanceStatus = "p";
        console.log(found.Name + " is now Present");
    }
    else {
        console.log("Participant with registration number " + regNo + " not found");
    }
}

markAttendance(102);

console.log(participants);


// 5. Generate Event Summary

function eventSummary() {

    let totalParticipants = participants.length;

    let paidParticipants = participants.filter(function (v) {
        return v.paymentStatus === "paid";
    }).length;

    let unpaidParticipants = participants.filter(function (v) {
        return v.paymentStatus === "not paid";
    }).length;

    let presentParticipants = participants.filter(function (v) {
        return v.attendanceStatus === "p";
    }).length;

    let absentParticipants = participants.filter(function (v) {
        return v.attendanceStatus === "a";
    }).length;


    console.log("----- EVENT SUMMARY -----");
    console.log("Total Participants: " + totalParticipants);
    console.log("Paid Participants: " + paidParticipants);
    console.log("Unpaid Participants: " + unpaidParticipants);
    console.log("Present Participants: " + presentParticipants);
    console.log("Absent Participants: " + absentParticipants);
}

eventSummary();