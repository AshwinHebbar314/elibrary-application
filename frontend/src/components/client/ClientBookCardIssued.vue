<script setup>
import store from '@/store';
</script>

<template>
    <!-- {{ book }} -->
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
                    <p class="card-text"><small class="text-body-secondary"><b>Issue Date:</b> {{
                        book.issue_date }}</small></p>
                    <p class="card-text"><small class="text-body-secondary"><b>Due Date:</b> {{
                        book.expiry_date }}</small></p>
                    <div class="p-2"><a :href="bookLink" class="btn btn-primary">View Details</a></div>
                    <div class="p-2"><a :href="getContentURL(this.book.content_path)" class="btn btn-success">Read</a>
                    </div>
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
            bookLink: `/book/${this.book.id}`,
            readbook: ""
        }
    },
    methods:
    {
        getCoverURL(value) {
            return `${store.getters.BASEURL}/static/covers/${value}`
        },
        getContentURL(value) {
            return `${store.getters.BASEURL}/static/books/${value}`
        }
    }
}
</script>