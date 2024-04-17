<script setup>
import store from '@/store';
import UpdateBookEntry from '@/views/admin/UpdateBookEntry.vue';
</script>

<template>
    <div class="card m-3" style="max-width: 540px;">
        <div class="row g-0">
            <div class="col-md-4">
                <img :src="getCoverURL(book.cover_path)" class="img-fluid rounded-start"
                    style="height: 198px; width: 170px;">
            </div>
            <div class="col-md-8">
                <div class="card-body">
                    <h5 class="card-title">{{ book.title }}</h5>
                    <p class="card-text">{{ book.author }}</p>
                    <p class="card-text"><small class="text-body-secondary">Last updated: {{ book.last_issued }}</small></p>
                    <!-- button to delete book -->
                    <button type="button" class="btn btn-danger m-2" @click="deleteBook(book.id)">Delete</button>
                    <!-- button to update book -->
                    <UpdateBookEntry :currentBook="book" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ["book"],
    data() {
        return {
            msg: "",
            class: "",
            popup: false
        }
    },
    methods:
    {
        getCoverURL(value) {
            return `${store.getters.BASEURL}/static/covers/${value}`
        },
        deleteBook(id) {
            console.log("Deleting book with id:", id)
            fetch(store.getters.BASEURL + "/admin/book/delete" + "/" + id, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken
                },

            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    if (data.status == "success") {
                        console.log("Book deleted successfully");
                        // reload the page
                        window.location.reload();
                    }
                    else {
                        alert("Error: " + data.error);
                    }
                })
        }
    }
}
</script>