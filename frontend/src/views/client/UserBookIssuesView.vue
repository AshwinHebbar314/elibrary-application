<script setup>
import ClientNavbar from "@/components/ClientNavbar.vue";
import store from "@/store";
</script>

<template>
    <ClientNavbar />
    <!-- {{ books }} -->
    <div class="container p-3">
        <h1>My Issued Books</h1>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th scope="col">Issue ID</th>
                    <th scope="col">Title</th>
                    <th scope="col">Issue Date</th>
                    <th scope="col">Due Date</th>
                    <th scope="col">Read Book</th>
                    <th scope="col">Return Book</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="book in books || orderBy - 1" :key="book.id">
                    <td>{{ book.book_issue_id }}</td>
                    <td>{{ book.title }}</td>
                    <td>{{ book.issue_date }}</td>
                    <td>{{ book.expiry_date }}</td>
                    <td v-if="book.issue_status != 'returned'">
                        <a :href="getPDFURL(book.content_path)" target="_blank" class="btn btn-primary">Read</a>
                    </td>
                    <td v-else>
                        <button class="btn btn-primary" disabled>Read</button>
                    </td>
                    <td v-if="book.issue_status != 'returned'">
                        <button class="btn btn-primary" @click="returnBook(book.book_issue_id)">Return</button>
                    </td>
                    <td v-else>
                        <button class="btn btn-primary" disabled>Returned</button>
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
            books: [],
        }
    },
    methods: {
        getIssuedBooks() {
            console.log("Fetching issued books");
            fetch(store.getters.BASEURL + "/mybooks", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken
                },
                body: JSON.stringify({
                    userID: store.getters.getUserID
                })
            })
                .then(response => response.json())
                .then(data => {
                    this.books = data;
                })
                .catch(error => {
                    console.error("Error: ", error);
                })
        },
        returnBook(bookissueID) {
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
                    this.getIssuedBooks();
                })
                .catch(error => {
                    console.error("Error: ", error);
                })

        },
        getPDFURL(value) {
            return `${store.getters.BASEURL}/static/books/${value}`
        }
    },
    created() {
        this.getIssuedBooks();
    }
}
</script>

