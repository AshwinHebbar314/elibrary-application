<script setup>
import { RouterView } from 'vue-router';
import AdminNavbar from '@/components/AdminNavbar.vue';
// import store from "@/store";
</script>

<template>
    <AdminNavbar />
    <RouterView />
</template>

<script>
export default {
    data() {
        return {

        }
    },
    methods: {

    }
}
</script>