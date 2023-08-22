<script>
    let url = "http://localhost:8000/"
    // http://daily-be.k8s.jeromeswannack.com/
    // ensure url has trailing slash
    if (url[url.length - 1] !== '/') url += '/';

    let report = {
        happiness: 5,
        tiredness: 5,
        notable_events: "",
        notes: ""
    };

    async function submit(event) {
        event.preventDefault();
        if (!event.target.checkValidity()) return;
        try {
            console.log(report);
            const response = await fetch(`${url}reports/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    report: report
                })
            });
            const data = await response.json();
            console.log(data);
        } catch(error) {
            console.log(error);
        }
    }
</script>

<h2>Daily Self Report</h2>
<form on:submit={submit}>
    <label for="happiness">Happiness</label>
    <input type="range" id="happiness" bind:value={report.happiness} min="1" max="10" required />

    <label for="tiredness">Tiredness</label>
    <input type="range" id="tiredness" bind:value={report.tiredness} min="1" max="10" required />

    <label for="notable_events">Notable events</label>
    <textarea id="notable_events" bind:value={report.notable_events} required ></textarea>

    <label for="notes">Notes</label>
    <textarea id="notes" bind:value={report.notes} required></textarea>

    <button type="submit">Submit</button>
</form>

<style>
    /* place index.css equivalent styles here */
</style>
