<script setup>
import ClientNavbar from '@/components/ClientNavbar.vue'
import store from '@/store'
</script>

<template>
    <ClientNavbar />
    <div class="logreg-card container border position-absolute top-50 start-50 translate-middle p-3 rounded">

        <h2 class="d-flex justify-content-center p-3">Register as a new User</h2>

        <form @submit="signup">

            <div class="row">
                <div class="col">
                    <input type="text" class="form-control" placeholder="First name" aria-label="First name"
                        v-model="fname">
                </div>
                <div class="col">
                    <input type="text" class="form-control" placeholder="Last name" aria-label="Last name" v-model="lname">
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-4">
                    <input type="text" class="form-control" placeholder="Username" aria-label="Username" v-model="uname">
                </div>
                <div class="col-8">
                    <input type="email" class="form-control" placeholder="Email" aria-label="Email" v-model="email">
                </div>
            </div>
            <div class="row mt-3">
                <div class="col">
                    <input type="password" class="form-control" placeholder="Password" aria-label="Password" v-model="pass">
                </div>
            </div>
            <div class="row mt-3">
                <div class="col">
                    <input type="password" class="form-control" placeholder="PasswordConfirm" aria-label="PasswordConfirm"
                        v-model="passconf">
                </div>
            </div>

            <div class="row mt-3">
                <div class="col">
                    <button type="submit" class="btn btn-primary">Register</button>
                </div>
            </div>
            <div class="mt-3 alert alert-danger" role="alert" v-if="errstatus">
                Error: {{ output }}
            </div>
        </form>

    </div>
</template>

<script>
export default {
    data() {
        return {
            fname: '',
            lname: '',
            uname: '',
            email: '',
            pass: '',
            passconf: '',

            errstatus: false, // for error message
            output: '', //store error messages
        }
    },
    methods: {
        validate() {
            if (this.fname === '' || this.lname === '' || this.uname === '' || this.email === '' || this.pass === '' || this.passconf === '') {
                // alert('All fields are required')
                this.output = 'All fields are required'
                return false
            }
            if (this.fname.length < 3) {
                // alert('First name must be at least 3 characters')
                this.output = 'First name must be at least 3 characters'
                return false
            }
            if (this.uname.length < 3) {
                // alert('Username must be at least 3 characters')
                this.output = 'Username must be at least 3 characters'
                return false
            }
            if (this.pass !== this.passconf) {
                // alert('Passwords do not match')
                this.output = 'Passwords do not match'
                return false
            }
            // check for email format using regex
            const emailRegex = /^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$/;
            if (!emailRegex.test(this.email)) {
                // alert('Invalid email format')
                this.output = 'Invalid email format'
                return false
            }
            return true
        },
        signup(event) {
            event.preventDefault()
            if (this.validate()) {
                console.log('Validation Successful')
                console.log(this.fname, this.lname, this.uname, this.email, this.pass, this.passconf)
                fetch(store.getters.BASEURL + "/signup", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        fname: this.fname,
                        lname: this.lname,
                        uname: this.uname,
                        email: this.email,
                        pass: this.pass,
                        passconf: this.passconf,
                    }),
                })
                    .then((response) => response.json())
                    .then((data) => {
                        console.log(data)
                        if (data.status === 'success') {
                            console.log('Registration successful')
                            this.$router.push('/signin')
                        }
                        else {
                            // alert(data.error)
                            this.output = data.error
                            this.errstatus = true
                        }
                    })
                    .catch((error) => {
                        console.error('Error:', error)

                    })
            }
        }
    }
}
</script>

<style scoped></style>