<link rel="stylesheet" href="./chart.css">
<script>
	import Chart from './Chart.svelte';

	let data;
	let updateMode = undefined;
	let tlen = 0
	let tdays = 0
	let gwidth = 100;

	async function loaddata() {		
		const settings = {
        	method: 'POST',
        	headers: {
            	Accept: 'application/json',
            	'Content-Type': 'application/json',
        	},
			body: JSON.stringify({hrstoshow: hrstoshow, daysago: daysago})
    	};
		const response = await fetch('/data',settings)
		data = await response.json();
		tlen = Math.min(data["totallength"],168)
		tdays = Math.ceil(data["totallength"]/24)
	}

	import { onMount } from 'svelte';
	onMount(async () => {
		loaddata()
		setInterval(function() {
			updateMode = "none"
			loaddata()
		},10000)
	})

	let hrstoshow = 3
	let daysago = 0

	function chgrange() {
		loaddata()
	}

	function mousezoom(e) {
		if (e.deltaY < 0)
			gwidth = Math.min(6000,gwidth*2)
		else if (e.deltaY > 0 && gwidth > 100)
			gwidth = Math.max(100,gwidth/2)
	}

</script>
Show {hrstoshow} Hours: <input type="range" min="1" max="{tlen}" bind:value="{hrstoshow}" on:change="{chgrange}">
Ending {daysago} Days Ago: <input type="range" min="0" max="{tdays}" bind:value="{daysago}" on:change="{chgrange}">
<main>
	<div class="chart" style="width:{gwidth}vh" on:mousewheel="{mousezoom}">
		<Chart {data} {updateMode}/>	
	</div>
</main>
