<script setup>
import store from '@/store';
import ClientNavbar from '@/components/ClientNavbar.vue';
</script>

<template>
    <ClientNavbar />
    <!-- {{ userDetails }} -->
    <div class="container p-3">
        <h1>User Profile</h1>
        <div class="container border rounded p-3">
            <form @submit="updateProfile">
                <div class="row">
                    <h3>Name</h3>
                    <div class="col">
                        <input type="text" class="form-control" placeholder="First name" aria-label="First name"
                            v-model="userDetails.fname">
                    </div>
                    <div class="col">
                        <input type="text" class="form-control" placeholder="Last name" aria-label="Last name"
                            v-model="userDetails.lname">
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col-4">
                        <h5>Username</h5>
                        <input type="text" class="form-control" placeholder="Username" aria-label="Username"
                            v-model="userDetails.uname" disabled>
                    </div>
                    <div class="col-8">
                        <h5>Email</h5>
                        <input type="email" class="form-control" placeholder="Email" aria-label="Email"
                            v-model="userDetails.email">
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col">
                        <h5>Password</h5>
                        <input type="password" class="form-control" placeholder="Password" aria-label="Password"
                            v-model="userDetails.pass">
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col">
                        <h5>Confirm Password</h5>
                        <input type="password" class="form-control" placeholder="PasswordConfirm"
                            aria-label="PasswordConfirm" v-model="userDetails.passconf">
                    </div>
                </div>
                <div class="row mt-3">
                    <div class="col">
                        <button type="submit" class="btn btn-warning">Update</button>
                    </div>
                </div>
            </form>
            <div class="mt-3 alert alert-danger" role="alert" v-if="msgstatus">
                Error: {{ msg }}
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            userID: store.getters.getUserID,
            userDetails: {},

            msg: "",
            msgstatus: false,
            msgclass: "",
        }
    },
    methods: {
        getProfileDetails() {
            fetch(store.getters.BASEURL + "/user/get/" + this.userID, {
                method: "GET",
                headers: {
                    "Authentication-Token": store.getters.getToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    this.userDetails = data

                })
                .catch(error => {
                    console.error("Error: ", error);
                    this.msg = error
                    this.msgstatus = true
                    this.msgclass = "alert alert-danger"
                })
        },
        validate() {
            if (this.pass !== this.passconf) {
                this.msgstatus = true;
                this.msg = "Passwords do not match";
                return false;
            }
            if (this.fname === '' || this.lname === '' || this.email === '' || this.pass === '' || this.passconf === '') {
                this.msgclass = true;
                this.msg = "All fields are required";
                return false;
            }
            return true;
        },
        updateProfile(event) {
            event.preventDefault();
            if (this.validate()) {
                fetch(store.getters.BASEURL + "/user/update", {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authentication-Token": store.getters.getToken
                    },
                    body: JSON.stringify({
                        "userID": store.getters.getUserID,
                        "fname": this.userDetails.fname,
                        "lname": this.userDetails.lname,
                        "email": this.userDetails.email,
                        "pass": this.userDetails.pass,
                        "passconf": this.userDetails.passconf
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        if (data.status == "success") {
                            this.msg = "Profile updated successfully";
                            this.msgstatus = true;
                            this.msgclass = "alert alert-success";
                        }
                        else {
                            this.msg = "Error: " + data.error;
                            this.msgstatus = true;
                            this.msgclass = "alert alert-danger";
                        }
                    })
                    .catch(error => {
                        console.error("Error: ", error);

                    })
            }
        },
    },
    mounted() {
        this.getProfileDetails();
    }
}
</script>