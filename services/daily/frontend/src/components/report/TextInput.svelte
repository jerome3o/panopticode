<script lang="ts">
    export let value: string = "";
    export let title: string = "Text Input";
</script>

<label for="textinput">{title}</label>
<textarea id="textinput" bind:value={value}></textarea>
