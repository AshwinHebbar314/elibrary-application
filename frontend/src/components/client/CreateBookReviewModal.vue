<script setup>
import store from '@/store';
</script>

<template>
    <!-- Button trigger modal -->
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createBookReviewModal">
        Submit Review
    </button>

    <!-- Modal -->
    <div class="modal fade" id="createBookReviewModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Write Your Review</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit="submitReview">
                        <div class="mb-3">
                            <label for="reviewTitle" class="form-label">Review Title</label>
                            <input type="text" class="form-control" id="reviewTitle" aria-describedby="reviewTitleHelp"
                                v-model="reviewTitle">
                            <div id="reviewTitleHelp" class="form-text">Mandatory</div>
                        </div>
                        <div class="mb-3">
                            <label for="review" class="form-label">Review</label>
                            <textarea class="form-control" id="review" rows="3" v-model="reviewDesc"></textarea>
                        </div>
                        <div class="mb-3">
                            <label for="customRange3" class="form-label">Score</label>
                            <input type="range" class="form-range" min="1" max="10" step="1" id="customRange3"
                                v-model="reviewScore">
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="submit" class="btn btn-primary">Submit Review</button>
                        </div>
                    </form>
                </div>
                <div :class="msgClass" role="alert" v-if="msgStatus">
                    {{ msg }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            reviewTitle: "",
            reviewDesc: "",
            reviewScore: 5,

            reviews: [],

            msg: "",
            msgClass: "",
            msgStatus: false,

        }
    },
    methods: {
        validateReview() {
            if (this.reviewTitle === "" || this.reviewDesc === "") {
                this.msg = "Please fill in all the fields";
                this.msgClass = "alert alert-danger";
                this.msgStatus = true;
                return false;
            }
            return true;

        },
        submitReview(event) {
            console.log(this.reviewTitle, this.reviewDesc, this.reviewScore);
            event.preventDefault();
            if (this.validateReview()) {
                console.log("Frontend Create Review Validation Successful.")
                fetch(store.getters.BASEURL + "/book/review/" + store.getters.getUserID, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authentication-Token": store.getters.getToken

                    },
                    body: JSON.stringify({
                        bookID: this.$route.params.id,
                        reviewTitle: this.reviewTitle,
                        reviewDesc: this.reviewDesc,
                        reviewScore: this.reviewScore
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status == "success") {
                            console.log(data);
                            this.msg = "Review Submitted Successfully!";
                            this.msgClass = "alert alert-success";
                            this.msgStatus = true;
                        }
                        else {
                            console.error("Error: ", data.error);
                            this.msg = data.error;
                            this.msgClass = "alert alert-danger";
                            this.msgStatus = true;
                        }
                    })
                    .catch(error => {
                        console.error("Error: ", error);
                        this.msg = "Error: " + error;
                        this.msgClass = "alert alert-danger";
                        this.msgStatus = true;
                    });
            }

        },

    },
}
</script>
