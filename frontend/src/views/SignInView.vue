<script setup>
import ClientNavbar from "@/components/ClientNavbar.vue";
import store from "@/store";

</script>

<template>
    <ClientNavbar />
    <!-- <h2>{{ store.state.message }}</h2> -->

    <div class="logreg-card container border position-absolute top-50 start-50 translate-middle p-3 rounded">

        <h2 class="d-flex justify-content-center p-3">Login to your account</h2>

        <form @submit="signin">

            <div class="row">
                <div class="col">
                    <input type="text" class="form-control" placeholder="Username" aria-label="Username" v-model="uname">
                </div>
            </div>
            <div class="row mt-3">
                <div class="col">
                    <input type="password" class="form-control" placeholder="Password" aria-label="Password" v-model="pass">
                </div>
            </div>
            <div class="row mt-3">
                <div class="col">
                    <button type="submit" class="btn btn-primary">Login</button>
                </div>
            </div>
            <div class="mt-3 alert">
                <div class="alert alert-danger" role="alert" v-if="errstatus">
                    Error: {{ output }}
                </div>
            </div>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            uname: "",
            pass: "",

            errstatus: false,
            output: "",

            user: store.state.user,
        }
    },
    methods: {
        validate() {
            if (this.uname == "" || this.pass == "" || this.uname.length < 3) {
                this.errstatus = true;
                this.output = "Please fill in all fields";
                return false;
            }
            return true;
        },

        signin(event) {
            event.preventDefault();
            if (this.validate()) {
                console.log("Frontend Login Validation Successful.")
                console.log("Username: ", this.uname, "Password: ", this.pass)
                fetch(store.getters.BASEURL + "/signin", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        uname: this.uname,
                        pass: this.pass,
                    }),
                })
                    .then((response) => response.json())
                    .then((data) => {
                        console.log(data);
                        if (data.status == "success") {
                            console.log("Login Successful");
                            this.user.token = data.token;
                            this.user.roles = data.roles;
                            this.user.username = data.name;
                            this.user.user_id = data.id;
                            store.commit("setUser", this.user);
                            // console.log("Token in data.token: ", data.token)
                            // console.log("Token in state store: ", store.state.user.token);
                            this.$router.push("/"); // Redirect to Home after successful login
                        } else {
                            console.log("Login Failed");
                            this.errstatus = true;
                            this.output = data.error;
                        }
                    })
            }
        }
    }
}

</script>
