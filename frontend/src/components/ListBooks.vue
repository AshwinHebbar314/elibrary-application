<script setup>
import BookCard from './BookCard.vue';
import store from '@/store';
</script>

<template>
    <div class="container p-3">
        <h1>All Books</h1>
        <div class="row">
            <form class="d-flex" role="search" @submit="searchBook">
                <input class="form-control me-2" type="text" placeholder="Search" aria-label="Search" v-model="searchQuery">
                <select class="form-select me-2" aria-label="Large select example" v-model="searchField">
                    <option value="title" selected>title</option>
                    <option value="author">author</option>
                    <option value="section">section</option>
                </select>
                <button class="btn btn-outline-success me-2" type="submit">Search</button>
            </form>
            <BookCard v-for="book in books" :key="book.id" :book="book" />
        </div>
        <div class="p-3"><a class="btn btn-primary" href="/admin/book/create" role="button">Create a book entry</a></div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            books: [],
            booksoriginal: [],
        }
    },
    methods: {
        fetchBooks() {
            console.log("Fetching books");
            fetch(store.getters.BASEURL + "/admin/book/getList", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken
                }
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
        this.fetchBooks();
    }
}
</script>