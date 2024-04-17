<script setup>
import { RouterView } from 'vue-router'
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "bootstrap/dist/css/bootstrap.min.css";
import "@/assets/custom.css"
import store from "@/store";
</script>

<template>
    <RouterView />
</template>

<script>
export default {
    created() {
        let user = JSON.parse(sessionStorage.getItem("user"));

        if (user === null) {
            user = {
                token: "",
                roles: []
            }

        }
        store.commit("setUser", user);
    }
}
</script>
