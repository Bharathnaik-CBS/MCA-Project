document.addEventListener("DOMContentLoaded", () => {
  const proIdSelect = document.getElementById("proIdSelect");
  const proNameSelect = document.getElementById("proNameSelect");

  let projectMap = [];

  // Load project data from Flask
  fetch("/get-projects")
    .then(res => res.json())
    .then(data => {
      if (data.error) throw new Error(data.error);

      projectMap = data;

      // Populate both dropdowns
      data.forEach(proj => {
        const idOption = new Option(proj.pro_id, proj.pro_id);
        const nameOption = new Option(proj.pro_name, proj.pro_id); // same value as ID

        proIdSelect.add(idOption);
        proNameSelect.add(nameOption);
      });

      // Sync proNameSelect with proIdSelect
      proIdSelect.addEventListener("change", () => {
        proNameSelect.value = proIdSelect.value;
      });

      // Sync proIdSelect with proNameSelect
      proNameSelect.addEventListener("change", () => {
        proIdSelect.value = proNameSelect.value;
      });
    })
    .catch(err => {
      document.getElementById("plot-error-msg").textContent = "Error loading projects: " + err;
    });

  // Submit handler
  document.getElementById("plotForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    fetch("/add-plot", {
      method: "POST",
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          alert(`Plot ${data.plot_no} added successfully!`);
          this.reset();
          document.getElementById("plot-error-msg").textContent = "";
        } else {
          document.getElementById("plot-error-msg").textContent = "Error: " + data.error;
        }
      })
      .catch(err => {
        document.getElementById("plot-error-msg").textContent = "Unexpected error: " + err;
      });
  });
});
