<script>
    import Slider from "./Slider.svelte";
    import TextInput from "./TextInput.svelte";

    export let report = {
        happiness: 5,
        tiredness: 5,
        notable_events: "",
        notes: ""
    };
</script>

<Slider title="Happiness" bind:value={report.happiness}/>
<Slider title="Tiredness" bind:value={report.tiredness}/>
<TextInput title="Notable Events" bind:value={report.notable_events} />
<TextInput title="Notes" bind:value={report.notes}/>
