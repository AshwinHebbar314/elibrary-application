<script setup>
import oneReviewforBook from "@/components/client/oneReviewForBook.vue";
</script>

<template>
    <div class="container-fluid">
        <h2>Reviews</h2>
        <p>Here's what the people say about this book:</p>
        <!-- {{ reviews }} -->
        <div class="">
            <div class="row">
                <oneReviewforBook v-for="review in reviews" :key="review.id" :review="review" />
            </div>
        </div>

    </div>
</template>

<script>
export default {
    props: ['reviews'],
    data() {

    }
}
</script>