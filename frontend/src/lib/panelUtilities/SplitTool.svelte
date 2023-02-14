<script>
  import Currency from "../Currency.svelte";
  import { Button } from "carbon-components-svelte";
  import CurrencyInput from "../CurrencyInput.svelte";
  import Time from "svelte-time";
  import { split } from "../../api";
  import { transaction_to_split } from "../stores";

  function add() {
    split_array = split_array.concat(0);
  }
  function subtract() {
    split_array = split_array.slice(0, -1);
  }
  $: split_array = [0, 0];

  function trigger_split() {
    split($transaction_to_split?.id, split_array);
    split_array = [0, 0];
    $transaction_to_split = null;
  }
</script>

<div>
  Split "{$transaction_to_split?.description}
  (<Time timestamp={$transaction_to_split?.date} format="MM/DD" />)" <br />
  into <strong>{split_array.length}</strong> transactions:
  <br />
  <br />
  <div>
    <Button
      size="small"
      kind="tertiary"
      iconDescription="Subtract a row"
      on:click={add}>+ Add</Button
    >
    <Button
      kind="tertiary"
      disabled={split_array.length <= 2}
      size="small"
      on:click={subtract}>- Subtract</Button
    >
  </div>
  <br />
  {#each split_array as a}
    <CurrencyInput bind:value={a} />
  {/each}
  <br />
  <strong
    >Total: <Currency
      value={split_array.reduce((a, b) => a + b, 0).toString()}
    /></strong
  >
  (
  <Currency
    value={(
      $transaction_to_split?.amount - split_array.reduce((a, b) => a + b, 0)
    ).toString()}
  /> remaining )
  <br />
  <br />
  <div>
    <Button
      kind="tertiary"
      on:click={() => ($transaction_to_split = null)}
      type="submit">Cancel</Button
    >
    <Button
      kind="secondary"
      disabled={$transaction_to_split?.amount !=
        split_array.reduce((a, b) => a + b, 0) && split_array.includes(0)}
      on:click={trigger_split}
      type="submit">Split</Button
    >
  </div>
</div>
