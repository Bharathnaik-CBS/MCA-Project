function displayErrorMessage() {
    const errorBox = document.getElementById("error-box");
    const countdown = document.getElementById("countdown");
    let seconds = 3;
    errorBox.style.display = "block";

    const interval = setInterval(() => {
        seconds--;
        countdown.textContent = seconds;
        if (seconds <= 0) {
            clearInterval(interval);
            window.location.href = "/";
        }
    }, 1000);
}
