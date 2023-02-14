<script>
  import { transaction_query_params } from "./stores";
  import { Search } from "carbon-components-svelte";
  import { getTransactions } from "../api";

  let search = "";
  $: $transaction_query_params = { search: search };
  //Debounce the search
  let timeout;
  $: {
    if (timeout) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(() => {
      getTransactions($transaction_query_params);
    }, 200);
  }
</script>

<Search size="sm" placeholder="Search transactions..." bind:value={search} />
