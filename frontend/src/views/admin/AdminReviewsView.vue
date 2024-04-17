<script setup>
import listOfReviewsForAdmin from '@/components/admin/listOfReviewsForAdmin.vue';
import store from '@/store';
</script>

<template>
    <div class="container p-3">
        <h1>All Reviews</h1>
        <listOfReviewsForAdmin :reviews="reviews" />
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
            fetch(store.getters.BASEURL + "/admin/getreviews", {
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