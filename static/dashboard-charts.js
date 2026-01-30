let overallChart;

async function updateOverallChart(start, end) {
    const loading = document.getElementById('overall-loading');
    loading.style.display = 'block';

    try {
        const res = await fetch(`/api/overall-analytics?start=${start}&end=${end}`);
        const data = await res.json();

        const chartData = {
            labels: data.labels,
            datasets: [
                {
                    label: 'Bulk Leads Reach',
                    data: data.leads,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Incoming',
                    data: data.incoming,
                    backgroundColor: 'rgba(255, 206, 86, 0.6)',
                    borderColor: 'rgba(255, 206, 86, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Interest',
                    data: data.interest,
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }
            ]
        };

        const config = {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Overall Analytics'
                    },
                    datalabels: {
                        anchor: 'end',
                        align: 'top',
                        formatter: Math.round
                    }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            },
            plugins: [ChartDataLabels]
        };

        if (overallChart) overallChart.destroy();
        overallChart = new Chart(document.getElementById('overallChart'), config);

    } catch (err) {
        console.error("Error loading overall chart:", err);
    } finally {
        loading.style.display = 'none';
    }
}


let platformChart;

async function updatePlatformChart(start, end) {
    const loading = document.getElementById('platform-loading');
    loading.style.display = 'block';

    try {
        const res = await fetch(`/api/platform-analytics?start=${start}&end=${end}`);
        const data = await res.json();

        const chartData = {
            
            labels: data.labels, // platform names
            datasets: [{
                label: 'Bulk Leads Reach',
                data: data.leads, // only leads
                backgroundColor: [
                    'rgba(255, 99, 132, 0.6)',
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 206, 86, 0.6)',
                    'rgba(75, 192, 192, 0.6)',
                    'rgba(153, 102, 255, 0.6)',
                    'rgba(255, 159, 64, 0.6)'
                ],
                borderColor: '#fff',
                borderWidth: 1
            }]
        };
    data.leads = data.leads.map(val => Number(val));

        const config = {
            type: 'pie',
            data: chartData,
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Platform-Wise Leads Distribution'
                    },
                    datalabels: {
                        formatter: (value, ctx) => {
                            const sum = ctx.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / sum) * 100).toFixed(1) + '%';
                            return percentage;
                        },
                        color: '#000',
                        anchor: 'end',
                        align: 'start'
                    }
                }
            },
            plugins: [ChartDataLabels]
        };

        if (platformChart) platformChart.destroy();
        platformChart = new Chart(document.getElementById('platformChart'), config);

    } catch (err) {
        console.error("Error loading platform chart:", err);
    } finally {
        loading.style.display = 'none';
    }
}


let employeeChart;

async function updateEmployeeChart(start, end) {
    const loading = document.getElementById('employee-loading');
    loading.style.display = 'block';

    try {
        const res = await fetch(`/api/employee-analytics?start=${start}&end=${end}`);
        const data = await res.json();

        const chartData = {
            labels: data.labels,
            datasets: [
                {
                    label: 'Bulk Leads Reach',
                    data: data.leads,
                    backgroundColor: 'rgba(255, 99, 132, 0.6)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Incoming',
                    data: data.incoming,
                    backgroundColor: 'rgba(255, 205, 86, 0.6)',
                    borderColor: 'rgba(255, 205, 86, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Interest',
                    data: data.interest,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }
            ]
        };

        const config = {
            type: 'bar',
            data: chartData,
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Employee-Wise Analytics'
                    },
                    datalabels: {
                        anchor: 'end',
                        align: 'top',
                        formatter: Math.round
                    }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            },
            plugins: [ChartDataLabels]
        };

        if (employeeChart) employeeChart.destroy();
        employeeChart = new Chart(document.getElementById('employeeChart'), config);

    } catch (err) {
        console.error("Error loading employee chart:", err);
    } finally {
        loading.style.display = 'none';
    }
}


let projectChart;

async function updateProjectChart(start, end) {
    const loading = document.getElementById('project-loading');
    loading.style.display = 'block';

    try {
        const res = await fetch(`/api/project-analytics?start=${start}&end=${end}`);
        const data = await res.json();

        const chartData = {
            labels: data.labels,
            datasets: [
                {
                    label: 'Bulk Leads Reach',
                    data: data.leads,
                    backgroundColor: 'rgba(201, 203, 207, 0.6)',
                    borderColor: 'rgba(201, 203, 207, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Incoming',
                    data: data.incoming,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Interest',
                    data: data.interest,
                    backgroundColor: 'rgba(255, 159, 64, 0.6)',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    borderWidth: 1
                }
            ]
        };

        const config = {
            type: 'bar',
            data: chartData,
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Project-Wise Analytics'
                    },
                    datalabels: {
                        anchor: 'end',
                        align: 'top',
                        formatter: Math.round
                    }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            },
            plugins: [ChartDataLabels]
        };

        if (projectChart) projectChart.destroy();
        projectChart = new Chart(document.getElementById('projectChart'), config);

    } catch (err) {
        console.error("Error loading project chart:", err);
    } finally {
        loading.style.display = 'none';
    }
}



document.getElementById('update-all').addEventListener('click', () => {
    const start = document.getElementById('global-start').value;
    const end = document.getElementById('global-end').value;

    if (!start || !end) {
        alert("Please select both start and end dates.");
        return;
    }

    updateOverallChart(start, end);
    updatePlatformChart(start, end);
    updateEmployeeChart(start, end);
    updateProjectChart(start, end);
});
