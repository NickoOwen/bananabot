let currentDate = new Date();

// TODO Get banana time from the backend (from /banana-time)
let bananaTime = "15:30:00";

// Split the time into hours, minutes and seconds
let splitTime = bananaTime.split(':');

// Set the count down date accordingly
let countDownDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate(), splitTime[0], splitTime[1], splitTime[2]);

// Set the count down date to the following day if it is already past banana time
if (currentDate > countDownDate) {
    countDownDate.setDate(countDownDate.getDate() + 1);
}

console.log(countDownDate)

// Update the count down every 1 second
let x = setInterval(function() {
    // Get today's date and time
    let now = new Date().getTime();

    // Find the time between now and the count down date
    let timeDelta = countDownDate - now;

    // Time calculations for hours, minutes and seconds
    let hours = Math.floor((timeDelta % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    let minutes = Math.floor((timeDelta % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((timeDelta % (1000 * 60)) / 1000);

    // console.log("Hours: " + hours);
    // console.log("Mins: " + minutes);
    // console.log("Secs: " + seconds);

    // Update the respective HTML
    document.getElementById("timer-hours").innerHTML = hours;
    document.getElementById("timer-mins").innerHTML = minutes;
    document.getElementById("timer-secs").innerHTML = seconds;

    // Do something once the countdown has finished
    // if (timeDelta < 0) {
    //   clearInterval(x);
    //   document.getElementById("demo").innerHTML = "EXPIRED";
    // }

    // TODO Either reset the timer or do some cool animation if a user is viewing the timer during banana time
}, 1000);