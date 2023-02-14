<script>
  import "./lib/TransactionTable.svelte";
  import StackList from "./lib/StackList.svelte";
  import SidePanel from "./lib/SidePanel.svelte";
  import Header from "./lib/Header.svelte";
  import Main from "./lib/Main.svelte";
  import "carbon-components-svelte/css/all.css";
</script>

<main class="parent">
  <div class="header"><Header /></div>
  <div class="stacks"><StackList /></div>
  <div class="main"><Main /></div>
  <div class="side_panel"><SidePanel /></div>
</main>

<style>
  .parent {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    grid-template-rows: 50px 65px repeat(3, 1fr);
    grid-column-gap: 5px;
    grid-row-gap: 5px;
  }

  .header {
    grid-area: 1 / 1 / 2 / 6;
  }
  .stacks {
    grid-area: 2 / 1 / 6 / 2;
  }
  .main {
    grid-area: 2 / 2 / 6 / 5;
  }
  .side_panel {
    grid-area: 2 / 5 / 6 / 6;
  }
</style>
