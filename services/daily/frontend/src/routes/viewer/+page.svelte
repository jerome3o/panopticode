<script lang="ts">
	import Plotly from 'plotly.js/dist/plotly.js';
	import { onMount } from 'svelte';

	let url: string = import.meta.env.VITE_BACKEND_URL;

	let plotElement;

	onMount(() => {
		fetch(`${url}reports/`).then((data) => {
			return data.json().then((data) => {
				const layout = {
					title: 'Line and Scatter Plot'
				};
				console.log(data);

				const trace1 = {
					x: data.map((x) => x['created_timestamp']),
					y: data.map((x) => x['report']['happiness']),
					mode: 'lines',
					type: 'scatter'
				};

				Plotly.newPlot(plotElement, [trace1], layout);
			});
		});
	});
</script>

<h1>Hey test</h1>
<div bind:this={plotElement} id="tester" style="width:100%;height:100%;" />
