<script setup>
import ClientNavbar from '@/components/ClientNavbar.vue';
import listOfReviewsForUser from '@/components/client/listOfReviewsForUser.vue';
import store from '@/store';
</script>

<template>
    <ClientNavbar />
    <div class="container p-3">
        <h1>My Book Reviews</h1>
        <listOfReviewsForUser :reviews="reviews" />
    </div>
</template>

<script>
export default {
    data() {
        return {
            reviews: []
        }
    },
    methods: {
        getReviewsForUser() {
            fetch(store.getters.BASEURL + "/book/reviews/user/" + store.getters.getUserID, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    this.reviews = data;

                })
                .catch(error => {
                    console.error("Error: ", error);
                })
        }

    },
    created() {
        this.getReviewsForUser();
    },
}
</script>