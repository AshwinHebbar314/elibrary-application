<script setup>
import store from '@/store';
</script>

<template>
    <div class="card m-3" style="max-width: min(520px, 95vw) ">
        <div class="row">
            <div class="col d-flex flex-wrap align-items-center">
                <img :src="getCoverURL(book.cover_path)" class="img-fluid rounded-start"
                    style="height: 198px; width: 170px;">
            </div>
            <div class="col">
                <div class="card-body">
                    <h5 class="card-title">{{ book.title }}</h5>
                    <p class="card-text">{{ book.author }}</p>
                    <p class="card-text"><b>Section:</b> {{ book.section }}</p>
                    <p class="card-text"><small class="text-body-secondary"><b>Last updated:</b> {{
                        book.last_issued }}</small></p>
                    <a :href="bookLink" class="btn btn-primary">View Details</a>
                </div>
            </div>
        </div>
    </div>
    <!-- </div> -->
</template>

<script>
export default {
    props: ["book"],
    data() {
        return {
            msg: "",
            class: "",
            popup: false,
            bookLink: `/book/${this.book.id}`
        }
    },
    methods:
    {
        getCoverURL(value) {
            return `${store.getters.BASEURL}/static/covers/${value}`
        },
    }
}
</script>