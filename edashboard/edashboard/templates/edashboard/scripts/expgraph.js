{% load staticfiles %}
console.log('{{ date }}');
  var myChart = new Chart(document.getElementById("line-chart"), {
    type: 'line',
    data: {
      labels: [{% for data in date %}
                    {{ data }},
                  {% endfor %}],
      fillOpacity: .3,
      datasets: [{
          data: [{% for data in usage %}
                        {{ data }},
                        {% endfor %}],
          label: "Week 1",
          borderColor: "#1f61a8",
          fill: origin,
          backgroundColor: "rgba(31,97,168,.3)",
        },
      ]
    },
    options: {
      responsive: false,
      title: {
        display: true,
        text: "SAS Building Electricity usage",
      },
      scales: {
      xAxes: [{
        scaleLabel: {
          display: true,
          labelString: 'Time'
        }
      }],
      yAxes: [{
        scaleLabel: {
          display: true,
          labelString: 'Electricity (kWh)'
        }
      }]
    }
    }
  }
);
