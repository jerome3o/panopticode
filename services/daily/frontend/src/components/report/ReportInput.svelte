<script>
    import Slider from "./Slider.svelte";
    import TextInput from "./TextInput.svelte";

    export let report = {
        happiness: 50,
        tiredness: 50,
        stress: 50,
        notes: ""
    };

    let min = 0;
    let max = 100;
</script>

<Slider title="Happiness" bind:value={report.happiness} {min} {max}/>
<Slider title="Tiredness" bind:value={report.tiredness} {min} {max}/>
<Slider title="Stress" bind:value={report.stress} {min} {max}/>
<TextInput title="Notes" bind:value={report.notes}/>
