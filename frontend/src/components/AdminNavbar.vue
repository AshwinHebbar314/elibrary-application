<script setup>
import { RouterLink } from 'vue-router';
import store from '@/store';
</script>

<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <router-link class="navbar-brand" to="/admin"><b>Admin</b> @ eLib</router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
                aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link class="nav-link active" aria-current="page" to="/admin/sections">Sections</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/admin/books">Books</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/admin/book/requests">Book Requests</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/admin/book/issues">Book Issues</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/admin/reviews">Book Reviews</router-link>
                    </li>
                </ul>
                <button @click="exportCSVUser" class="btn btn-outline-dark mx-2">Export User Data</button>
                <button @click="exportCSVBooks" class="btn btn-outline-dark mx-2">Export Books Data</button>
                <button class="btn btn-danger mx-2" @click="signout">Signout</button>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    data() {
        return {
            user: store.state.user,
            task_id: null,
            error: {
                export: null
            }
        }
    },
    methods: {
        signout() {
            console.log("Signing out");
            fetch(store.getters.BASEURL + "/signout", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    this.user.roles = [];
                    this.user.token = null;
                    this.user.username = null;
                    this.user.user_id = null;
                    store.commit("setUser", this.user);
                    this.$router.push("/signin");
                })
                .catch(error => {
                    console.error("Error: ", error);
                })
        },
        exportCSVUser() {
            fetch(store.getters.BASEURL + "/export/users", {
                method: "GET",
                headers: {
                    "Authentication-Token": store.getters.getToken
                }
            }).then(response => {
                if (response.status == 200)
                    return response.json()
                return {}
            }).then(data => {
                if (Object.keys(data).includes("id")) {
                    this.task_id = data["id"]
                    this.getExportStatusUser()
                }
            })
        },
        getExportStatusUser() {
            fetch(store.getters.BASEURL + "/export/users?task=" + this.task_id, {
                method: "GET",
                headers: {
                    "Authentication-Token": store.getters.getToken
                }
            }).then(response => {
                if (response.status == 200) {
                    return response.json()
                }
                else {
                    this.error['export'] = "Export job failed."
                    return {}
                }
            }).then(data => {
                if (Object.keys(data).includes("status")) {
                    if (data["status"] == "SUCCESS") {
                        open(store.getters.BASEURL + "/download/users?task=" + this.task_id)
                    } else {
                        setTimeout(this.getExportStatusUser, 1000);
                    }
                }
            })
        },
        exportCSVBooks() {
            fetch(store.getters.BASEURL + "/export/books", {
                method: "GET",
                headers: {
                    "Authentication-Token": store.getters.getToken
                }
            }).then(response => {
                if (response.status == 200)
                    return response.json()
                return {}
            }).then(data => {
                if (Object.keys(data).includes("id")) {
                    this.task_id = data["id"]
                    this.getExportStatusBooks()
                }
            })
        },
        getExportStatusBooks() {
            fetch(store.getters.BASEURL + "/export/books?task=" + this.task_id, {
                method: "GET",
                headers: {
                    "Authentication-Token": store.getters.getToken
                }
            }).then(response => {
                if (response.status == 200) {
                    return response.json()
                }
                else {
                    this.error['export'] = "Export job failed."
                    return {}
                }
            }).then(data => {
                if (Object.keys(data).includes("status")) {
                    if (data["status"] == "SUCCESS") {
                        open(store.getters.BASEURL + "/download/books?task=" + this.task_id)
                    } else {
                        setTimeout(this.getExportStatusBooks, 1000);
                    }
                }
            })
        },

    }
}
</script>