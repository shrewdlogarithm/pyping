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

  </script>
  
  <Line {data} {options} {updateMode}/>
  