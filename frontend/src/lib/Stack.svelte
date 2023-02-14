<script>
  import {
    ProgressBar,
    Tile,
    Accordion,
    AccordionItem,
  } from "carbon-components-svelte";
  import { fly, fade } from "svelte/transition";
  import { quintOut } from "svelte/easing";
  import Currency from "./Currency.svelte";
  import { Button } from "carbon-components-svelte";
  import { stack_to_edit } from "./stores";
  export let stack;
</script>

<div class="stack_box">
  <div class="stack_row title">
    <button
      on:click={() => {
        $stack_to_edit = stack;
      }}
    >
      {stack.name}
    </button>
    {#key stack.total}
      <span
        class="numbers right"
        in:fly={{ y: -8, duration: 500, easing: quintOut }}
      >
        <Currency
          color={stack.total < 0
            ? "var(--cds-text-error)"
            : "var(--cds-text-01)"}
          value={stack.total.toString()}
        />
      </span>
    {/key}
  </div>
  {#if stack.goal}
    <progress max={stack.goal} value={stack.total} class="progress" />
    <div class="stack_row">
      <span>Goal:</span>
      <Currency
        color="var(--cds-ui-text01), black"
        value={stack.goal.toString()}
      />
    </div>
  {/if}
  {#if stack.budget}
    {#key stack.budget + stack.spent}
      <div class="stack_row">
        <span>Budget:</span>
        <Currency
          color="var(--cds-ui-text01)"
          value={stack.budget.toString()}
        />
      </div>
      <div class="stack_row">
        <span>Spent:</span>
        <Currency
          color="var(--cds-support-01)"
          value={stack.spent.toString()}
        />
      </div>
      <div class="stack_row">
        <span>Remaining:</span>
        <Currency
          color="var(--cds-ui-text01), black"
          value={(Number(stack.budget) + Number(stack.spent)).toString()}
        />
      </div>
    {/key}
  {/if}
</div>

<style>
  button {
    padding: 0;
    border: none;
    background: none;
    font-weight: bold;
    cursor: pointer;
    color: var(--cds-text-01);
  }
  .title {
    font-weight: bold;
  }
  .stack_box {
    padding: 0.5rem;
    background-color: var(--cds-ui-01, #f4f4f4);
    border-bottom: 1px solid var(--cds-border-strong);
  }
  .stack_row {
    padding: 2px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  progress {
    display: block;
    width: 100%;
    border-radius: 0;
    border: none;
    height: 3px;
    background: none;
  }
</style>
