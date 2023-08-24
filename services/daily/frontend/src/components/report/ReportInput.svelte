<script>
    import Slider from "./Slider.svelte";
    import TextInput from "./TextInput.svelte";

    export let report = {
        happiness: 50,
        tiredness: 50,
        notable_events: "",
        notes: ""
    };

    let min = 0;
    let max = 100;
</script>

<Slider title="Happiness" bind:value={report.happiness} {min} {max}/>
<Slider title="Tiredness" bind:value={report.tiredness} {min} {max}/>
<TextInput title="Notable Events" bind:value={report.notable_events} />
<TextInput title="Notes" bind:value={report.notes}/>
