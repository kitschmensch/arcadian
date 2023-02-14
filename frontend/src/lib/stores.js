import { writable } from 'svelte/store';

//Data Stores
export const transactions = writable([]);
export const stacks = writable([]);
export const tenant = writable([]);
export const transaction_query_params = writable({});

//Side Panel States
export const side_panel_state = writable([]);
export const transaction_to_split = writable(null);
export const stack_to_edit = writable(null);


