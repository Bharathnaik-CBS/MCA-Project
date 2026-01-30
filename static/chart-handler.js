function fetchMetrics(route, chartId, labelPrefix) {
  const start = document.getElementById("start").value;
  const end = document.getElementById("end").value;

  fetch(route, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ start, end })
  })
  .then(res => res.json())
  .then(data => {
    const ctx = document.getElementById(chartId).getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Bulk Leads", "Incoming", "Interest"],
        datasets: [{
          label: labelPrefix + " Metrics",
          data: [data.bulk, data.incoming, data.interest],
          backgroundColor: ["#007bff", "#ffc107", "#28a745"]
        }]
      }
    });
  });
}
