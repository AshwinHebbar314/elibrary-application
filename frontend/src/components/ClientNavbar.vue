<script setup>
// import RouterLink from 'vue-router'
import store from '@/store';
</script>

<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="/">eLib</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link class="nav-link active" aria-current="page" to="/">Home</router-link>
                    </li>
                    <li class="nav-item" v-if="store.getters.getToken === null">
                        <router-link class="nav-link active" aria-current="page" to="/signup">Sign Up</router-link>
                    </li>
                    <li class="nav-item" v-if="store.getters.getToken !== null">
                        <router-link class="nav-link active" aria-current="page" to="/myprofile">My Profile</router-link>
                    </li>
                    <li class="nav-item" v-if="store.getters.getToken !== null">
                        <router-link class="nav-link active" aria-current="page" to="/mybooks">My Books</router-link>
                    </li>
                    <li class="nav-item" v-if="store.getters.getToken !== null">
                        <router-link class="nav-link active" aria-current="page" to="/mybookrequests">Book
                            Requests</router-link>
                    </li>
                    <li class="nav-item" v-if="store.getters.getToken !== null">
                        <router-link class="nav-link active" aria-current="page" to="/mybookissues">Issued
                            Books</router-link>
                    </li>
                    <li class="nav-item" v-if="store.getters.getToken !== null">
                        <router-link class="nav-link active" aria-current="page" to="/myreviews">Book Reviews</router-link>
                    </li>
                </ul>
                <button class="btn btn-danger" @click="signout">Signout</button>


                <!-- <form class="d-flex" role="search">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form> -->
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    data() {
        return {
            user: store.state.user
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
        }
    }
}
</script>