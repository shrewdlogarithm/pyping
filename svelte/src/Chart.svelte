<script>
    import { Line } from 'svelte-chartjs';
  
    export let data;
    export let updateMode;

    export let options = {
      scales: {   
        x: {
          display: true,
        },
        y: {
          display: true,
          type: 'logarithmic'
        }
      },
      responsive: true,
      maintainAspectRatio: false
    }

    import {
      Chart as ChartJS,
      Title,
      Tooltip,
      Legend,
      LineElement,
      LinearScale,
      PointElement,
      CategoryScale,
      LogarithmicScale
    } from 'chart.js';
  
    ChartJS.register(
      Title,
      Tooltip,
      Legend,
      LineElement,
      LinearScale,
      PointElement,
      CategoryScale,
      LogarithmicScale
    );

    let chart
    // setInterval(function() {
    //   console.log(chart,data)
    //   data.datasets[0].hidden = !data.datasets[0].hidden
    // },1000)
  </script>
  
  <Line bind:chart {data} {options} {updateMode}/>
  