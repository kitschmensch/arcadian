<script>
  import Currency from "./Currency.svelte";
  import { tenant } from "./stores";
  import { onMount } from "svelte";
  import { getTenant } from "../api";
  onMount(async () => {
    getTenant();
  });
</script>

<style>
  .title {
    font-weight: bold;
    border-bottom: 1px solid black;
  }
  .stack_box {
    padding: 0.75rem;
    background-color: white;
    border-top: 1px solid black;
  }
  .stack_row {
    padding: 3px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
</style>
