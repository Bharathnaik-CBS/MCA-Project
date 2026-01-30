
  document.getElementById("projectForm").addEventListener("submit", function (e) {
    e.preventDefault(); // Prevent default form submission

    const formData = new FormData(this);

    fetch("/add-project", {
      method: "POST",
      body: formData
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          alert(`Project ${data.pro_name} (${data.pro_id}) added successfully!`);
          this.reset();
          document.getElementById("project-error-msg").textContent = "";
        } else {
          document.getElementById("project-error-msg").textContent = "Error: " + data.error;
        }
      })
      .catch((err) => {
        document.getElementById("project-error-msg").textContent = "Unexpected error: " + err;
      });
  });
