<script lang="ts">
    export let value: number = 5;
    export let title: string = "Slider Value";
    export let min: number = 1;
    export let max: number = 10;

</script>

<label for="slider">{title}</label>
<input type="range" id="slider" bind:value {min} {max} required />
