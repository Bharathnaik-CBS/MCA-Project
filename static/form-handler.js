async function fetchTransactionId() {
  const res = await fetch("/get-latest-tid");
  const data = await res.json();
  document.getElementById("transaction-id").value = data.t_id;
}

function setTodayDate() {
  const dateInput = document.getElementById("date");
  if (dateInput) {
    dateInput.value = new Date().toISOString().split("T")[0];
  }
}

function toggleForms() {
  const transactionBtn = document.getElementById("showTransaction");
  const entriesBtn = document.getElementById("showEntries");

  const transactionForm = document.getElementById("transactionForm");
  const entriesForm = document.getElementById("entriesForm");

  transactionBtn.addEventListener("click", () => {
    transactionForm.style.display = "block";
    entriesForm.style.display = "none";
    fetchTransactionId();
    setTodayDate();
  });

  entriesBtn.addEventListener("click", () => {
    transactionForm.style.display = "none";
    entriesForm.style.display = "block";
  });
}

function handleFormSubmit(formId, url) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    try {
      const res = await fetch(url, {
        method: "POST",
        body: formData
      });
      const result = await res.json();

      const msgDiv = document.getElementById(`${formId}_msg`);
      if (formId === "transactionForm" && result.status === "success") {
  alert("Transaction submitted!");
  form.reset();
  msgDiv.textContent = "";

  // Fill t_id into Entries Form
  const entryTIdField = document.getElementById("entry-transaction-id");
  if (entryTIdField) {
    entryTIdField.value = result.t_id;
  }

  // Automatically show entries form
  document.getElementById("transactionForm").style.display = "none";
  document.getElementById("entriesForm").style.display = "block";
}

      else {
        msgDiv.textContent = result.message || "Submission failed!";
        msgDiv.style.color = "red";
      }
    } catch (err) {
      console.error(err);
    }
  });
}

async function populateDropdowns() {
  const [empRes, projRes, platRes] = await Promise.all([
    fetch("/get-employees"), fetch("/get-projects"), fetch("/get-platforms")
  ]);

  const employees = await empRes.json();
  const projects = await projRes.json();
  const platforms = await platRes.json();

  const empIdSelect = document.getElementById("emp_id");
  const empNameSelect = document.getElementById("emp_name");
  const projIdSelect = document.getElementById("project_id");
  const projNameSelect = document.getElementById("project_name");
  const platIdSelect = document.getElementById("platform_id");
  const platTypeSelect = document.getElementById("platform_type");

  if (empIdSelect && empNameSelect) {
    employees.forEach(emp => {
      empIdSelect.add(new Option(emp.e_id, emp.e_id));
      empNameSelect.add(new Option(emp.e_name, emp.e_id));
    });
    empIdSelect.addEventListener("change", () => {
      empNameSelect.value = empIdSelect.value;
    });
    empNameSelect.addEventListener("change", () => {
      empIdSelect.value = empNameSelect.value;
    });
  }

  if (projIdSelect && projNameSelect) {
    projects.forEach(p => {
      projIdSelect.add(new Option(p.pro_id, p.pro_id));
      projNameSelect.add(new Option(p.pro_name, p.pro_id));
    });
    projIdSelect.addEventListener("change", () => {
      projNameSelect.value = projIdSelect.value;
    });
    projNameSelect.addEventListener("change", () => {
      projIdSelect.value = projNameSelect.value;
    });
  }

  if (platIdSelect && platTypeSelect) {
    platforms.forEach(p => {
      platIdSelect.add(new Option(p.p_id, p.p_id));
      platTypeSelect.add(new Option(p.p_types, p.p_id));
    });
    platIdSelect.addEventListener("change", () => {
      platTypeSelect.value = platIdSelect.value;
    });
    platTypeSelect.addEventListener("change", () => {
      platIdSelect.value = platTypeSelect.value;
    });
  }
}




window.addEventListener("DOMContentLoaded", () => {
  toggleForms();
  handleFormSubmit("transactionForm", "/add-transaction");
  handleFormSubmit("entriesForm", "/add-entry");
  populateDropdowns(); //  load dropdowns on page load
});
