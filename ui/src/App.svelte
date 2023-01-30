<script lang="ts">
  import Counter from "./lib/Counter.svelte";
  import Transaction from "./lib/Transaction.svelte";
</script>

<main>
  <list>
    <Counter />
    <Counter />
    <Counter />
  </list>
  <Transaction />
  <div>
    <Counter />
    <Counter />
    <Counter />
  </div>
</main>

<style>
  main {
    display: flex;
  }
</style>
