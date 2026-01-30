document.getElementById("customerForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const formData = new FormData(this);

  fetch("/add-customer", {
    method: "POST",
    body: formData
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        alert(`Customer ${data.cust_name} added successfully!`);
        this.reset();
        document.getElementById("customer-error-msg").textContent = "";
      } else {
        document.getElementById("customer-error-msg").textContent = "Error: " + data.error;
      }
    })
    .catch((err) => {
      document.getElementById("customer-error-msg").textContent = "Unexpected error: " + err;
    });
});
