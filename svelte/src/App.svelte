<link rel="stylesheet" href="./chart.css">
<script>
	import Chart from './Chart.svelte';

	let data = {datasets: []};
	let updateMode = undefined;
	let tlen = 0
	let tdays = 0
	let gwidth = 100;

	let ahosts = []

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
		ahosts = []
		data["datasets"].forEach(function(ds) {
			ahosts.push({"ds": ds,"active": data["activehosts"].includes(ds.label)})
		})
		tlen = Math.max(data["totallength"],1)
		tdays = Math.ceil(data["totallength"]/24)
		setTimeout(function() {
			updateMode = "none"
			loaddata()
		},10000)
	}

	import { onMount } from 'svelte';
    import { claim_component } from 'svelte/internal';
	onMount(async () => {
		loaddata()
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

	async function handleclick (host,dsn) {
		const res = await fetch('/toglhost', {
			method: 'POST',
			body: host
		})
		data["datasets"][dsn].enabled = !data["datasets"][dsn].enabled 
	}

	let newhost = ""
	async function addhost() {
		const res = await fetch('/addhost', {
			method: 'POST',
			body: newhost
		})
	}

</script>
Show {hrstoshow} Hours: <input type="range" min="1" max="{tlen}" bind:value="{hrstoshow}" on:change="{chgrange}">
Ending {daysago} Days Ago: <input type="range" min="0" max="{tdays}" bind:value="{daysago}" on:change="{chgrange}">
{#each ahosts as ds,n}
	<input style="color: {ds["ds"].borderColor};float: left" type="checkbox" id="cb{ds["ds"].label}" checked={ds["active"]} on:click={() => handleclick(ds["ds"].label,n)}/><label style="float: left" for="cb{ds["ds"].label}">{ds["ds"].label}</label>
{/each}
<form on:submit={() => addhost()}>
	<input bind:value={newhost} />
</form>
<main>
	<div class="chart" style="width:{gwidth}vh" on:mousewheel="{mousezoom}">
		<Chart {data} {updateMode}/>	
	</div>
</main>