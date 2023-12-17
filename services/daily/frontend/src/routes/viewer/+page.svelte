<script lang="ts">
	import Plotly from 'plotly.js/dist/plotly.js';
	import { onMount } from 'svelte';

	let url: string = import.meta.env.VITE_BACKEND_URL;

	let plotElement;
	let text = 'Hover over a data point to see the report';

	onMount(() => {
		fetch(`${url}reports/`).then((data) => {
			return data.json().then((data) => {
				// sort data by created_timestamp

				data.sort((a, b) => {
					return a['created_timestamp'] - b['created_timestamp'];
				});

				const layout = {
					title: 'Line and Scatter Plot',
					yaxis_range: [0, 100]
				};

				const trace1 = {
					x: data.map((x) => x['created_timestamp']),
					y: data.map((x) => x['report']['happiness']),
					mode: 'lines',
					type: 'scatter'
				};

				Plotly.newPlot(plotElement, [trace1], layout);

				plotElement.on('plotly_hover', (event) => {
					var index = event.points[0].pointNumber;

					text = data[index].report.notes;
				});
				plotElement.on('plotly_click', (event) => {
					var index = event.points[0].pointNumber;

					text = data[index].report.notes;
				});
			});
		});
	});
</script>

<h1>Happiness Levels</h1>
<div bind:this={plotElement} id="tester" style="width:100%;height:100%;" />
<pre>{text}</pre>

<style>
	pre {
		white-space: pre-wrap;
	}
</style>
