const renderChart = (data, labels)=>{
    var ctx = document.getElementById('myChart4').getContext('2d');
    ctx.height = 10;
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Distribution of expense amount (in ₹) in previous month'
                },
                legend: {
                    display: false,
            }
            }
        }
    });
    };
    
    const getChartData = ()=>{
        console.log("fetching");
        fetch("/daywise-previous-month-report-display")
        .then((res)=>res.json())
        .then((results)=>{
            console.log("results", results);
            const chart_data = results.data
            const [labels, data] = 
            [Object.keys(chart_data),
            Object.values(chart_data)];
    
            renderChart(data, labels)
        });
    }
    
    document.onload = getChartData();