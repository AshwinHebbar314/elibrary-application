<script setup>
import ClientNavbar from '@/components/ClientNavbar.vue';
import ClientBookCardIssued from '@/components/client/ClientBookCardIssued.vue';
import store from '@/store';
</script>

<template>
    <ClientNavbar />
    <div class="container p-3">
        <h1>My Books</h1>
        <div class="container-fluid" style="max-width: 90vw;">
            <div class="row">
                <form class="d-flex" role="search" @submit="searchBook">
                    <input class="form-control me-2" type="text" placeholder="Search" aria-label="Search"
                        v-model="searchQuery">
                    <select class="form-select me-2" aria-label="Large select example" v-model="searchField">
                        <option value="title" selected>title</option>
                        <option value="author">author</option>
                        <option value="section">section</option>
                    </select>
                    <button class="btn btn-outline-success me-2" type="submit">Search</button>
                </form>
                <div class="d-flex row row-cols-auto justify-content-center align-items-end">
                    <ClientBookCardIssued v-for="book in books" :key="book.id" :book="book" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            books: [],
            booksoriginal: []
        }
    },
    methods: {
        getMyBooks() {
            console.log("Fetching books");
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
                    this.booksoriginal = data;
                    // this.transformData(this.sections)
                })
                .catch(error => {
                    console.error("Error: ", error);
                })
        },
        searchBook(event) {
            event.preventDefault();
            this.books = this.booksoriginal;
            console.log("Searching for book");
            this.books = this.books.filter(book => {
                return book[this.searchField].toLowerCase().includes(this.searchQuery.toLowerCase());
            });
            console.log("Books after search: ", this.books);

        }
    },
    created() {
        this.getMyBooks();
    }
}
</script>