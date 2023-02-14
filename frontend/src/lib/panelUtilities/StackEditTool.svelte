<script>
  import { stack_to_edit } from "../stores";
  import { Button, TextInput, Modal } from "carbon-components-svelte";
  import { editStack, createStack, deleteStack, moveStack } from "../../api";
  import Add from "carbon-icons-svelte/lib/Add.svelte";
  import Subtract from "carbon-icons-svelte/lib/Subtract.svelte";
  import TrashCan from "carbon-icons-svelte/lib/TrashCan.svelte";
  import CurrencyInput from "../CurrencyInput.svelte";
  import TransferTool from "../TransferTool.svelte";
  import { stacks } from "../stores";

  let stack_name = "";
  let stack_goal = 0;
  let stack_position = 0;
  let stack_budget = 0;
  let stack_autotransfer = 0;

  stack_to_edit.subscribe(() => {
    stack_name = $stack_to_edit?.name;
    stack_goal = $stack_to_edit?.goal;
    stack_budget = $stack_to_edit?.budget;
    stack_autotransfer = $stack_to_edit?.autotransfer;
    stack_position = $stack_to_edit?.position ? $stack_to_edit.position : 0;
  });

  function submit() {
    if ($stack_to_edit == "new") {
      console.log("stack goal:", stack_goal);
      createStack(
        stack_name,
        stack_goal,
        stack_budget,
        stack_autotransfer,
        stack_position
      );
    } else {
      moveStack($stack_to_edit.id, stack_position);
      editStack(
        $stack_to_edit.id,
        stack_name,
        stack_goal,
        stack_budget,
        stack_autotransfer
      );
    }
    $stack_to_edit = null;
  }

  function deleteThisStack() {
    deleteStack($stack_to_edit.id);
    $stack_to_edit = null;
  }

  let open = false;
</script>

<TextInput
  type="text"
  labelText="Stack Name"
  size="sm"
  bind:value={stack_name}
/>
<CurrencyInput bind:value={stack_goal} labelText="Goal" size="sm" />
<CurrencyInput bind:value={stack_budget} labelText="Budget" size="sm" />
{#if $stack_to_edit.isPile == false}
  <CurrencyInput
    bind:value={stack_autotransfer}
    labelText="Auto Transfer"
    size="sm"
  />
{/if}
<br />
<span class="buttons">Position:</span>
<div class="buttons">
  <Button
    size="small"
    kind="tertiary"
    tooltipPosition="top"
    tooltipAlignment="start"
    iconDescription="Decrease position"
    icon={Subtract}
    disabled={stack_position == 0}
    on:click={() => {
      if (stack_position > 0) {
        stack_position -= 1;
      }
    }}
  />
  <span class="position">{stack_position + 1}</span>
  <Button
    size="small"
    kind="tertiary"
    tooltipPosition="top"
    tooltipAlignment="end"
    iconDescription="Increase position"
    icon={Add}
    disabled={stack_position >= $stacks.length - 1}
    on:click={() => {
      stack_position += 1;
    }}
  />

  <br />
  <br />
  <Button
    on:click={() => {
      open = true;
    }}
    iconDescription="Delete"
    icon={TrashCan}
    size="small"
    disabled={$stack_to_edit == "new" || $stack_to_edit.isPile == true}
    kind="danger-tertiary"
  />
  <Button
    on:click={() => {
      $stack_to_edit = null;
    }}
    size="small"
    kind="secondary">Cancel</Button
  >
  <Button size="small" on:click={submit} kind="primary">Save</Button>
</div>
<hr />
<TransferTool />
<Modal
  danger
  bind:open
  modalHeading="Delete this stack"
  primaryButtonText="Delete"
  secondaryButtonText="Cancel"
  on:click:button--secondary={() => (open = false)}
  on:open
  on:close
  on:submit={() => {
    deleteThisStack();
    open = false;
  }}
>
  <p>
    This is a permanent action and cannot be undone. All actions currently
    associated with this stack will be reassigned to the default stack.
  </p>
</Modal>

<style>
  .buttons {
    text-align: center;
    margin: auto;
  }

  .position {
    margin: 0 1rem;
    font-weight: bolder;
  }
</style>
