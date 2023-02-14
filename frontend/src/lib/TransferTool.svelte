<script>
  import CurrencyInput from "./CurrencyInput.svelte";
  import { Dropdown, Button } from "carbon-components-svelte";
  import { stacks, stack_to_edit } from "./stores";
  import { transfer } from "../api";

  // Hacky way to get the first two stacks
  //set default values. Erase amount and set to first two stacks

  let amount;
  let from;
  let to;

  async function triggerTransfer() {
    transfer(from, to, amount);
    amount = 0;
  }

  stack_to_edit.subscribe(() => {
    if ($stack_to_edit != null && $stack_to_edit != "new") {
      from = $stack_to_edit.id;
      to = $stacks[0].id;
    }
  });
</script>

<div class="wrapper">
  <CurrencyInput size="sm" labelText="Transfer" bind:value={amount} />
  <Dropdown
    titleText="From"
    bind:selectedId={from}
    items={$stacks}
    itemToString={(item) => item.name}
  />
  <Dropdown
    titleText="To"
    bind:selectedId={to}
    items={$stacks}
    itemToString={(item) => item.name}
  />
  <br />
  <div class="transfer_button">
    <Button
      disabled={from === to || !amount}
      size="small"
      on:click={triggerTransfer}
      kind="primary">Transfer</Button
    >
  </div>
</div>

<style>
  .wrapper {
    margin: 0.5rem;
    background: var(--cds-ui-01);
  }
  .transfer_button {
    text-align: center;
  }
</style>
