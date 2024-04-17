<script setup>
import store from "@/store";
</script>

<template>
    <div class="conrainer-fluid">
        <div class="container-fluid rounded p-3">
            <div class="row">
                <div class="col-sm-6 mb-3 mb-sm-0">
                    <div class="card" width="70%">
                        <div class="card-body">
                            <h5 class="card-title">{{ review.book_title }}</h5>
                            <div class="d-flex col justify-content-start">
                                <div class="row p-2">
                                    <p class="card-text">{{ review.review_title }}</p>
                                </div>
                                <div class="row p-2">
                                    <div class="text-muted">:</div>
                                </div>
                                <div class="row p-2">
                                    <p class="card-text">{{ review.rating }}/10</p>
                                </div>
                            </div>
                            <p class="card-text"><small class="text-muted">{{ review.review_date }}</small></p>
                            <hr>
                            <p class="card-text">{{ review.review_desc }}.</p>
                            <button class="btn btn-danger" @click="deleteReview(review.id)">Delete Review</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ['review'],
    data() {
        return {

        }
    },
    methods: {
        deleteReview(review_id) {
            console.log("Deleting review with id:", review_id)
            fetch(store.getters.BASEURL + "/book/review/delete/" + review_id, {
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
                        console.log("Review deleted successfully");
                        // reload the page
                        window.location.reload();
                    }
                    else {
                        console.log("Review deletion failed");
                    }
                })
        }
    }
}
</script>