document.addEventListener('DOMContentLoaded', () => {
  const token = document.querySelector('body').dataset.token;
  fetch(`/api/v1/results/${token}`)
    .then(r=>r.json())
    .then(res => {
      const { coords, matches } = res.data;

      // SCATTER
      new Chart(
        document.getElementById('scatter-chart'),
        {
          type: 'scatter',
          data: {
            datasets: coords.map(pt=>({
              label: pt.label,
              data:[{x: pt.x, y: pt.y}],
              pointRadius: pt.label==="You"?7:5
            }))
          },
          options:{ scales:{ x:{min:-3,max:3}, y:{min:-3,max:3} } }
        }
      );

      // HORIZONTAL BAR
      new Chart(
        document.getElementById('bar-chart'),
        {
          type: 'bar',
          data: {
            labels: matches.map(m=>m.party),
            datasets:[{
              label: '% agree',
              data: matches.map(m=>m.score)
            }]
          },
          options:{ indexAxis:'y', scales:{ x:{min:0,max:100} } }
        }
      );
    });
});
