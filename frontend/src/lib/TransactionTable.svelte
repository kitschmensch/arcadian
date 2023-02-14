<script>
  import {
    editTransactionStack,
    deleteTransaction,
    recombineTransaction,
  } from "../api";
  import { transactions, stacks, transaction_to_split } from "./stores";
  import {
    Dropdown,
    DataTable,
    OverflowMenu,
    OverflowMenuItem,
    DataTableSkeleton,
  } from "carbon-components-svelte";
  import Time from "svelte-time";
  import Currency from "./Currency.svelte";

  let headers = [
    { key: "stack", value: "Stack" },
    { key: "date", value: "Date" },
    { key: "description", value: "Description" },
    { key: "amount", value: "Amount", columnMenu: true },
    { key: "overflow", empty: true },
  ];
</script>

<DataTable size="short" {headers} rows={$transactions}>
  <svelte:fragment slot="cell" let:row let:cell>
    {#if cell.key == "stack"}
      <Dropdown
        light
        size="sm"
        disabled={[row.transfer, row.split].some((x) => x)}
        selectedId={cell.value}
        items={$stacks}
        itemToString={(item) => {
          return item?.name;
        }}
        on:select={(e) => {
          editTransactionStack(row.id, e.detail.selectedId);
        }}
      />
    {:else if cell.key == "amount"}
      <div class="amount_with_options">
        <div class:split={row.split}>
          <Currency
            color={row.transfer
              ? "var(--cds-support-04)"
              : row.amount > 0
              ? "var(--cds-support-02)"
              : "var(--cds-text-01)"}
            value={cell.value}
          />
        </div>
      </div>
    {:else if cell.key == "date"}
      <Time timestamp={cell.value} format="MM/DD" />
    {:else if cell.key === "overflow"}
      <OverflowMenu>
        <OverflowMenuItem
          disabled={[row.transfer, row.split, row.split_from].some((x) => x)}
          text="Split"
          on:click={(e) => {
            transaction_to_split.set(row);
          }}
        />
        <OverflowMenuItem
          disabled={!row.split}
          on:click={(e) => {
            recombineTransaction(row.id);
          }}
          text="Recombine"
        />
        <OverflowMenuItem
          disabled={[!row.transfer, row.split, row.split_from].some((x) => x)}
          danger
          on:click={(e) => {
            deleteTransaction(row.id);
          }}
          text="Delete"
        />
      </OverflowMenu>
    {:else}
      <div class:split={row.split}>{cell.value}</div>
    {/if}
  </svelte:fragment>
</DataTable>

<style>
  .amount_with_options {
    display: flex;
    justify-content: end;
  }

  .split {
    font-style: italic;
    text-decoration: line-through;
  }
</style>
