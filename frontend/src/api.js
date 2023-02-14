

import axios from "axios";
import { transactions, stacks, tenant, transaction_query_params } from "./lib/stores";
axios.defaults.headers.post['X-CSRFToken'] = get_token()
axios.defaults.headers.patch['X-CSRFToken'] = get_token()
axios.defaults.headers.delete['X-CSRFToken'] = get_token()

function get_token() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the 'csrftoken' we want?
            if (cookie.substring(0, "csrftoken".length + 1) === "csrftoken" + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring("csrftoken".length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

export async function getTenant() {
    const response = await axios.get("/api/tenants/1/")
        .then(response => { return response.data; })
    if (response) {
        return tenant.set(response)
    }
}

export async function getStacks() {
    const response = await axios.get("/api/stacks/")
        .then(response => { return response.data; })
    if (response) {
        stacks.set(response)
    }
}

export async function getStack(stack_id) {
    const response = await axios.get(`/api/stacks/${stack_id}/`)
        .then(response => { return response.data; })
    return response;
}

export async function createStack(name, goal, budget, autotransfer, position) {
    const response = await axios.post("/api/stacks/", {
        name: name,
        goal: goal ? goal : 0,
        budget: budget ? budget : null,
        autotransfer: autotransfer ? autotransfer : null,
        position: position ? position : 0,
    })
        .then(response => {
            getStacks();
            return response.data;
        })
}

export async function deleteStack(stack_id) {
    const response = await axios.delete(`/api/stacks/${stack_id}/`)
        .then(response => {
            getStacks();
            return response.data;
        })
}

export async function editStack(stack_id, name, goal, budget, autotransfer) {
    const response = await axios.patch(`/api/stacks/${stack_id}/`, {
        name: name,
        goal: goal ? goal : null,
        budget: budget ? budget : null,
        autotransfer: autotransfer ? autotransfer : null,
    })
        .then(response => {
            getStacks();
            return response.data;
        })

}

export async function moveStack(stack_id, position) {
    const response = await axios.post(`/api/stacks/${stack_id}/move/${position}/`)
        .then(response => {
            return response.data;
        })
}

export async function autoTransfer() {
    const response = await axios.post(`/api/autotransfer/`)
        .then(response => {
            getStacks();
            getTransactions();
            return response.data;
        })
}



export async function getTransactions(queryParams) {
    const query = new URLSearchParams(queryParams).toString()
    const response = await axios.get(`/api/transactions/?${query}`)
        .then(response => { return response.data; })
    if (response) {
        transactions.set(response)
    }
}


export function editTransactionStack(transaction_id, stack_id) {
    return axios.patch(`/api/transactions/${transaction_id}/`, {
        stack: stack_id,
    })
        .then(response => {
            getStacks();
            return response.data;
        })
}

export function transfer(from, to, amount) {
    axios.post(`/api/stacks/${from}/transferto/${to}`, {
        amount: amount,
    })
        .then(response => {
            getStacks();
            getTransactions();
            return response;
        })
        .catch(error => {
            console.log(error);
        });
}

export async function deleteTransaction(transaction_id) {
    const response = await axios.delete(`/api/transactions/${transaction_id}/`)
        .then(response => {
            getTransactions();
            getStacks();
            return response.data;
        })
}

export async function split(transaction_id, amount_array) {
    const response = await axios.post(`/api/transactions/${transaction_id}/split`, amount_array)
        .then(response => {
            getTransactions();
            getStacks();
            return response.data;
        })
}

export async function recombineTransaction(transaction_id) {
    const response = await axios.post(`/api/transactions/${transaction_id}/recombine/`)
        .then(response => {
            getTransactions();
            return response.data;
        })
}
