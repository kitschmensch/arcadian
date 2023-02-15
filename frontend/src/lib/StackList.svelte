<script>
  import Stack from "./Stack.svelte";
  import { Button } from "carbon-components-svelte";
  import Add from "carbon-icons-svelte/lib/Add.svelte";
  import { getStacks, getTransactions, getTenant, autoTransfer } from "../api";
  import { onMount } from "svelte";
  import { stacks, stack_to_edit, tenant } from "./stores";
  import Currency from "./Currency.svelte";

  const flipDurationMs = 300;
  function handleDndConsider(e) {
    console.log(e.detail);
  }
  function handleDndFinalize(e) {
    console.log(e.detail);
  }
  onMount(async () => {
    getStacks();
    getTransactions();
    getTenant();
  });
</script>

<div class="stack_wrapper">
  <div class="stack_box">
    <div class="stack_row title">
      <span>Total</span>
      <Currency color="var(--cds-text-01)" value={$tenant.total?.toString()} />
    </div>
    <div class="stack_row">
      <span>Spent:</span>
      <Currency
        color="var(--cds-support-01)"
        value={$tenant.spent?.toString()}
      />
    </div>
    <div class="stack_row">
      <span>Earned:</span>
      <Currency
        color="var(--cds-support-02, green)"
        value={$tenant.earned?.toString()}
      />
    </div>
  </div>
  <div class="centered">
    <Button
      on:click={() => {
        $stack_to_edit = "new";
      }}
      kind="secondary"
      size="small"
    >
      <Add /> Add Stack
    </Button>
  </div>

  {#each $stacks as stack (stack.id)}
    <Stack {stack} />
  {/each}
  <div class="centered">
    <Button on:click={autoTransfer} kind="secondary" size="small"
      >Auto Transfer
    </Button>
  </div>
</div>

<style>
  .centered {
    text-align: center;
    padding: 0.5rem;
  }
  .stack_wrapper {
    padding: 0.5rem;
  }
  .title {
    font-weight: bold;
    border-bottom: 1px solid black;
  }
  .stack_box {
    padding: 0.5rem;
    background-color: var(--cds-ui-01, #f4f4f4);
    border-bottom: 1px solid black;
  }
  .stack_row {
    padding: 3px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
</style>
