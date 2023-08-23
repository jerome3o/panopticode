<script lang="ts">
	import ReportInput from "./report/ReportInput.svelte";

    let url: string = import.meta.env.VITE_BACKEND_URL;
    if (url[url.length - 1] !== '/') url += '/';

    let report = {
        happiness: 5,
        tiredness: 5,
        notable_events: "",
        notes: ""
    };

    let id: string;
    let buttonText: string;
    let buttonClass: string;

    let uploading: boolean = false;

    $: buttonText = id ? "Update" : "Submit";
    $: buttonClass = id ? "update" : "new";

    let promise = fetch(`${url}reports/today/`)
        .then(response => response.json())
        .then(data => {
            if (data.value) {
                report = data.value.report;
                id = data.value.id;
            }
        });

    async function submit(event: any) {
        event.preventDefault();
        if (!event.target.checkValidity()) return;

        uploading = true;
        if (id) {
            await submitUpdate();
        } else {
            await submitNew();
        }
        // just so it feels like something happened lol
        await new Promise(resolve => setTimeout(resolve, 200));
        uploading = false;
    }

    async function submitUpdate() {
        try {
            console.log(report);
            const response = await fetch(`${url}reports/${id}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    report: report
                })
            });
            const data = await response.json();
            id = data.id;
            console.log(data);
        } catch(error) {
            console.log(error);
        }
    }

    async function submitNew() {
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
            id = data.id;
            console.log(data);
        } catch(error) {
            console.log(error);
        }
    }
</script>

<main>
    <div id="app">

        <h2>Daily Self Report</h2>

        {#await promise}
            <p>...waiting</p>
        {:then v}
            {#if id}
                <p>Already submitted today</p>
            {:else}
                <p>Not submitted today</p>
            {/if}
            <form on:submit={submit}>
                <ReportInput bind:report={report} />
                {#if uploading}
                    <button type="submit" class="loading">
                        loading
                    </button>
                {:else}
                    <button type="submit" class="{buttonClass}">
                        {buttonText}
                    </button>
                {/if}
            </form>
        {:catch error}
            <p style="color: red">Something terrible has happened???? {error}</p>
        {/await}

    </div>
</main>

<style>
.new {
    background-color: green;
}
.update {
    background-color: blue;
}
.loading {
    background-color: grey;
    color: black;
}


:global(main) {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
    background-color: #f8f9fa;
    font-family: 'Arial', sans-serif;
}
:global(#app) {
    width: 90%;
    height: 90%;
}
:global(form) {
    display: flex;
    flex-direction: column;
    min-width: 100%;
    width: 100%;
    margin: 0 auto;
}
:global(label) {
    margin-top: 20px;
    font-weight: bold;
}
:global(textarea, input, button) {
    margin-top: 5px;
}
/* make the text area fill it's available space */
/* prevent it from growing horizontally */
:global(textarea) {
    flex-grow: 1;
    width: 100%;
    resize: vertical;
    height: 200px;
}
:global(button) {
    padding: 10px;
    background-color: #6c757d;
    color: #fff;
    border: none;
    cursor: pointer;
    margin-top: 20px;
}
</style>
