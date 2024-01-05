<script lang="ts">
	import Plotly from 'plotly.js/dist/plotly.js';
	import { onMount } from 'svelte';

	interface ReportData {
		id: number;
		happiness: number;
		notes: string;
	}

	interface Report {
		created_timestamp: string;
		report: ReportData;
	}

	let url: string = '/api/';

	let plotElement: HTMLDivElement;
	let text = 'Hover over a data point to see the report';

	onMount(() => {
		fetch(`${url}reports/`).then((data) => {
			return data.json().then((data) => {
				// sort data by created_timestamp, convert to datetime and compare
				data.sort((a: Report, b: Report) => {
					return a['created_timestamp'].localeCompare(b['created_timestamp']);
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
