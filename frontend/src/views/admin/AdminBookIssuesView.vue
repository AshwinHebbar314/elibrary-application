<script setup>
import store from "@/store"
</script>

<template>
    <!-- {{ issues }} -->
    <div class="container p-3">
        <h1>Book Issues</h1>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th scope="col">Issue ID</th>
                    <th scope="col">Title</th>
                    <th scole="col">Issued To</th>
                    <th scope="col">Issue Date</th>
                    <th scope="col">Return Date</th>
                    <th scope="col">Revoke</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="issue in issues" :key="issue.id">
                    <td>{{ issue.id }}</td>
                    <td>{{ issue.bookTitle }}</td>
                    <td>{{ issue.userName }}</td>
                    <td>{{ issue.issue_date }}</td>
                    <td v-if="issue.return_date != null">{{ issue.return_date }}</td>
                    <td v-else>Not Returned</td>
                    <td v-if="issue.return_date == null">
                        <button class="btn btn-danger" @click="revokeIssue(issue.id)">Revoke</button>
                    </td>
                    <td v-else>
                        <button class="btn btn-warning" disabled>returned</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    data() {
        return {
            issues: [],
        }
    },
    methods: {
        getAllRemainingIssues() {
            console.log("Fetching issued books");
            fetch(store.getters.BASEURL + "/admin/book/issue/getList", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.issues = data;
                })
                .catch(error => {
                    console.error("Error: ", error);
                })
        },
        revokeIssue(bookissueID) {
            console.log("Returning book");
            fetch(store.getters.BASEURL + "/book/return/" + store.getters.getUserID, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken
                },
                body: JSON.stringify({
                    bookIssueID: bookissueID
                })
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    this.getAllRemainingIssues()
                })
                .catch(error => {
                    console.error("Error: ", error);
                })

        },
    },
    created() {
        this.getAllRemainingIssues();
    }
}
</script>