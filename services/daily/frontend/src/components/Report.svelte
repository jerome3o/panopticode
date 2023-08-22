<script lang="ts">
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

    async function submit(event: any) {
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

<main>
    <div id="app">
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
    </div>
</main>

<style>
main {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
    background-color: #f8f9fa;
    font-family: 'Arial', sans-serif;
}
#app {
    width: 70%;
    height: 70%;
}
form {
    display: flex;
    flex-direction: column;
    min-width: 100%;
    width: 100%;
    margin: 0 auto;
}
label {
    margin-top: 20px;
    font-weight: bold;
}
textarea, input, button {
    margin-top: 5px;
}
/* make the text area fill it's available space */
/* prevent it from growing horizontally */
textarea {
    flex-grow: 1;
    width: 100%;
    resize: vertical;
    height: 200px;
}

button {
    padding: 10px;
    background-color: #6c757d;
    color: #fff;
    border: none;
    cursor: pointer;
    margin-top: 20px;
}

</style>
