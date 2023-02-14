<script>
  import TransactionTable from "./TransactionTable.svelte";
  import Filters from "./Filters.svelte";
  import StackEditTool from "./panelUtilities/StackEditTool.svelte";
  import StackBudgetTable from "./StackBudgetTable.svelte";
  import TransferTool from "./TransferTool.svelte";
  import { stack_to_edit } from "./stores";
</script>

<div class="main">
  {#if $stack_to_edit}
    <div class="stack_view">
      <div class="stack_edit">
        <StackEditTool />
      </div>
      {#if $stack_to_edit != "new"}
        <div class="stack_spent">
          <StackBudgetTable />
        </div>
      {/if}
    </div>
  {:else}
    <div>
      <Filters />
      <TransactionTable />
    </div>
  {/if}
</div>

<style>
  .main {
    margin-top: 0.5rem;
  }
  .stack_view {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: 1fr;
    grid-column-gap: 0px;
    grid-row-gap: 0px;
  }
  .stack_edit {
    grid-area: 1 / 1 / 2 / 2;
  }
  .stack_spent {
    grid-area: 1 / 2 / 2 / 4;
  }
</style>
