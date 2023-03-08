window.onload = function() {
    let currentDate = new Date();

    let bananaTime = document.getElementById("banana-time").innerHTML;

    // Split the time into hours and minutes
    let splitTime = bananaTime.split(':');

    // Set the count down date accordingly
    let countDownDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate(), splitTime[0], splitTime[1], 0);

    // Set the count down date to the following day if it is already past banana time
    if (currentDate > countDownDate) {
        countDownDate.setDate(countDownDate.getDate() + 1);
    }

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

        // Update the respective HTML
        document.getElementById("timer-hours").innerHTML = hours;
        document.getElementById("timer-mins").innerHTML = minutes;
        document.getElementById("timer-secs").innerHTML = seconds;

        // Do something once the countdown has finished
        if (timeDelta <= 0) {
            // TODO Something more exciting than this
            clearInterval(x);
            document.getElementById("banana-timer-container").innerHTML = `<h1 class="banana-time-announcement">BANANA TIME!</h1>`;
        }
    }, 1000);
}