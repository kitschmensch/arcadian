<script>
  let items = [
    { id: 1, date: "2021-01-01", description: "Banana", amount: 1000.0 },
    { id: 2, date: "2021-01-02", description: "Apple", amount: -2000.0 },
    { id: 3, date: "2021-01-03", description: "Orange", amount: 3000.0 },
    { id: 4, date: "2021-01-04", description: "Grape", amount: -4000.0 },
    { id: 5, date: "2021-01-05", description: "Pineapple", amount: 5000.0 },
    { id: 6, date: "2021-01-06", description: "Strawberry", amount: -6000 },
    { id: 7, date: "2021-01-07", description: "Watermelon", amount: 7000.0 },
    { id: 8, date: "2021-01-08", description: "Mango", amount: -8000.0 },
    { id: 9, date: "2021-01-09", description: "Peach", amount: 9000.0 },
    { id: 10, date: "2021-01-10", description: "Cherry", amount: -10000.0 },
    { id: 1, date: "2021-01-01", description: "Banana", amount: 1000.0 },
    { id: 2, date: "2021-01-02", description: "Apple", amount: -2000.0 },
    { id: 3, date: "2021-01-03", description: "Orange", amount: 3000.0 },
    { id: 4, date: "2021-01-04", description: "Grape", amount: -4000.0 },
    { id: 5, date: "2021-01-05", description: "Pineapple", amount: 5000.0 },
    { id: 6, date: "2021-01-06", description: "Strawberry", amount: -6000 },
    { id: 7, date: "2021-01-07", description: "Watermelon", amount: 7000.0 },
    { id: 8, date: "2021-01-08", description: "Mango", amount: -8000.0 },
    { id: 9, date: "2021-01-09", description: "Peach", amount: 9000.0 },
    { id: 10, date: "2021-01-10", description: "Cherry", amount: -10000.0 },
    { id: 1, date: "2021-01-01", description: "Banana", amount: 1000.0 },
    { id: 2, date: "2021-01-02", description: "Apple", amount: -2000.0 },
    { id: 3, date: "2021-01-03", description: "Orange", amount: 3000.0 },
    { id: 4, date: "2021-01-04", description: "Grape", amount: -4000.0 },
    { id: 5, date: "2021-01-05", description: "Pineapple", amount: 5000.0 },
    { id: 6, date: "2021-01-06", description: "Strawberry", amount: -6000 },
    { id: 7, date: "2021-01-07", description: "Watermelon", amount: 7000.0 },
    { id: 8, date: "2021-01-08", description: "Mango", amount: -8000.0 },
    { id: 9, date: "2021-01-09", description: "Peach", amount: 9000.0 },
    { id: 10, date: "2021-01-10", description: "Cherry", amount: -10000.0 },
    { id: 1, date: "2021-01-01", description: "Banana", amount: 1000.0 },
    { id: 2, date: "2021-01-02", description: "Apple", amount: -2000.0 },
    { id: 3, date: "2021-01-03", description: "Orange", amount: 3000.0 },
    { id: 4, date: "2021-01-04", description: "Grape", amount: -4000.0 },
    { id: 5, date: "2021-01-05", description: "Pineapple", amount: 5000.0 },
    { id: 6, date: "2021-01-06", description: "Strawberry", amount: -6000 },
    { id: 7, date: "2021-01-07", description: "Watermelon", amount: 7000.0 },
    { id: 8, date: "2021-01-08", description: "Mango", amount: -8000.0 },
    { id: 9, date: "2021-01-09", description: "Peach", amount: 9000.0 },
    { id: 10, date: "2021-01-10", description: "Cherry", amount: -10000.0 },
  ];
</script>

<table>
  <tr>
    <th scope="col">Date</th>
    <th scope="col">Description</th>
    <th scope="col">Amount</th>
  </tr>
  {#each items as item}
    <tr>
      <td>{item.date}</td>
      <td>{item.description}</td>
      <td>{item.amount}</td>
    </tr>
  {/each}
</table>

<style>
  table {
    border-collapse: collapse;
  }
  th,
  td {
    border: 1px solid black;
    padding: 5px 30px;
  }
</style>
