<script setup>
import ClientNavbar from "@/components/ClientNavbar.vue";
import store from "@/store";
</script>

<template>
    <ClientNavbar />
    <!-- {{ books }} -->
    <div class="container p-3">
        <h1>Book Requests</h1>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th scope="col">Book ID</th>
                    <th scope="col">Title</th>
                    <th scope="col">Request Date</th>
                    <th scope="col">Request Duration</th>
                    <th scope="col">Status</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="book in books" :key="book.id">
                    <td>{{ book.id }}</td>
                    <td>{{ book.title }}</td>
                    <td>{{ book.request_date }}</td>
                    <td>{{ secondsToDhms(book.request_duration) }}</td>
                    <td>{{ book.request_status }}</td>
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
        fetchBooks() {
            console.log("Fetching books");
            fetch(store.getters.BASEURL + "/myrequests", {
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
        secondsToDhms(seconds) {
            seconds = Number(seconds);
            var d = Math.floor(seconds / (3600 * 24));
            var h = Math.floor(seconds % (3600 * 24) / 3600);
            var m = Math.floor(seconds % 3600 / 60);
            var s = Math.floor(seconds % 60);

            var dDisplay = d > 0 ? d + (d == 1 ? " d " : " d ") : "";
            var hDisplay = h > 0 ? h + (h == 1 ? " h " : " h ") : "";
            var mDisplay = m > 0 ? m + (m == 1 ? " m " : " m ") : "";
            var sDisplay = s > 0 ? s + (s == 1 ? " s " : " s ") : "";
            return dDisplay + hDisplay + mDisplay + sDisplay;
        },
    },
    mounted() {
        this.fetchBooks();
    }
}
</script>