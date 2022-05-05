$(document).ready(function () {

    var script_tag = document.getElementById('charts');
    var start = script_tag.getAttribute("data");

    const config = {
        type: 'line',
        data: {
            labels: Array(30).fill("00:00:00"),
            // labels: Array(30).fill("0000-00-00 00:00:00"),
            datasets: [{
                label: "Temperature",
                backgroundColor: 'rgb(109, 89, 122)',
                borderColor: 'rgb(109, 89, 122)',
                data: Array(30).fill(null),
                fill: false,
            }],
        },
        options: {
            legend: {
                position: 'top'
            },
            responsive: true,
            title: {
                display: true,
                text: 'Temperature measurement'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }]
            }
        }
    };

    const context = document.getElementById('layanan').getContext('2d');

    const lineChart = new Chart(context, config);

    if (start.includes("on")){
        const source = new EventSource("/temp-data");

        source.onmessage = function (event) {
            const data = JSON.parse(event.data);
            if (config.data.labels.length === 30) {
                config.data.labels.shift();
                config.data.datasets[0].data.shift();
            }
            config.data.labels.push(data.time);
            config.data.datasets[0].data.push(data.value);
            lineChart.update();
            $(".sensor1").text("");
            $(".sensor1").text(Math.round(data.value*100)/100 +" \u00B0 C");
        }

    }

    // Pressure chart

    const config2 = {
        type: 'line',
        data: {
            // labels: Array(30).fill("0000-00-00 00:00:00"),
            labels: Array(30).fill("00:00:00"),
            datasets: [{
                label: "Barometric Pressure",
                backgroundColor: 'rgb(181, 101, 118)',
                borderColor: 'rgb(181, 101, 118)',
                data: Array(30).fill(null),
                fill: false,
            }],
        },
        options: {
            legend: {
                position: 'top'
            },
            responsive: true,
            title: {
                display: true,
                text: 'Barometric pressure measurement'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }]
            }
        }
    };

    const context2 = document.getElementById('layanan_subbagian').getContext('2d');

    const lineChart2 = new Chart(context2, config2);
    
    if (start.includes("on")){
        const source2 = new EventSource("/pressure-data");

        source2.onmessage = function (event) {
            const data = JSON.parse(event.data);
            if (config2.data.labels.length === 30) {
                config2.data.labels.shift();
                config2.data.datasets[0].data.shift();
            }
            config2.data.labels.push(data.time);
            config2.data.datasets[0].data.push(data.value);
            lineChart2.update();
            $(".sensor2").text("");
            $(".sensor2").text(Math.round(data.value * 100)/100 + " hPa");
        }
    }
    // Humidity chart

    const config3 = {
        type: 'line',
        data: {
            // labels: Array(30).fill("0000-00-00 00:00:00"),
            labels: Array(30).fill("00:00:00"),
            datasets: [{
                label: "Humidity",
                backgroundColor: 'rgb(229, 107, 111)',
                borderColor: 'rgb(229, 107, 111)',
                data: Array(30).fill(null),
                fill: false,
            }],
        },
        options: {
            legend: {
                position: 'top'
            },
            responsive: true,
            title: {
                display: true,
                text: 'Humidity measurement'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }]
            }
        }
    };

    const context3 = document.getElementById('layanan_subbagian3').getContext('2d');

    const lineChart3 = new Chart(context3, config3);

    if (start.includes("on")){
        const source3 = new EventSource("/humidity-data");

        source3.onmessage = function (event) {
            const data = JSON.parse(event.data);
            if (config3.data.labels.length === 30) {
                config3.data.labels.shift();
                config3.data.datasets[0].data.shift();
            }
            config3.data.labels.push(data.time);
            config3.data.datasets[0].data.push(data.value);
            lineChart3.update();
            $(".sensor3").text("");
            $(".sensor3").text(Math.round(data.value*100)/100 + "%  RH");
        }
    }
});
