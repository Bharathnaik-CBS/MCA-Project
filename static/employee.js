document.getElementById("employeeForm").addEventListener("submit", function (e) {
  e.preventDefault(); // Prevent page reload

  const formData = new FormData(this);

  fetch("/add-employee", {
    method: "POST",
    body: formData
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        alert(`Employee ${data.e_name} (${data.e_id}) entered successfully!`);
        this.reset(); // Reset the form
      } else {
        document.getElementById("error-msg").textContent = "Error: " + data.error;
      }
    })
    .catch((err) => {
      document.getElementById("error-msg").textContent = "Unexpected error: " + err;
    });
});







/*
document.getElementById("employeeForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Stop form from submitting normally

    const formData = new FormData(this);

    fetch("/add-employee", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Employee added successfully:\n" + 
                "ID: " + data.e_id + "\n" +
                "Name: " + data.e_name + "\n" +
                "Phone: " + data.p_no + "\n" +
                "Email: " + data.email
            );
            this.reset(); // Reset form
        } else {
            document.getElementById("errorBox").innerText = "Error: " + data.error;
        }
    })
    .catch(error => {
        document.getElementById("errorBox").innerText = "Unexpected error occurred.";
        console.error("Error:", error);
    });
});
*/