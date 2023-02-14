<script>
  import { transaction_to_split, stack_to_edit } from "./stores";
  import SplitTool from "./panelUtilities/SplitTool.svelte";
  import TransferTool from "./TransferTool.svelte";
</script>

{#if $transaction_to_split != null}
  <SplitTool />
{/if}
