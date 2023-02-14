<script>
  export let value = "0.00";
  export let color = "black";
  if (value == "0") {
    value = "0.00";
  }
</script>

{#if value[0] == "-"}
  <span style:color
    >{"-$" + value.substring(1).replace(/\B(?=(\d{3})+(?!\d))/g, ",")}</span
  >
{:else}
  <span style:color>{"$" + value.replace(/\B(?=(\d{3})+(?!\d))/g, ",")}</span>
{/if}

<style>
  span {
    font-family: "IBM Plex Mono", "Courier New", Courier, monospace;
  }
</style>
