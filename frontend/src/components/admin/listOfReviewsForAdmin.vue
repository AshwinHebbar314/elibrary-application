<script setup>
import oneReviewForAdmin from "@/components/admin/oneReviewForAdmin.vue";
</script>

<template>
    <div class="container-fluid border">
        <!-- {{ reviews }} -->
        <div class="">
            <div class="row">
                <oneReviewForAdmin v-for="review in reviews" :key="review.id" :review="review" />
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