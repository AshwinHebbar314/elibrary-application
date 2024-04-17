<script setup>
import ClientNavbar from "@/components/ClientNavbar.vue";
import store from "@/store";
import PageDoesNotExist from "@/components/PageDoesNotExist.vue";
import CreateBookReviewModal from "@/components/client/CreateBookReviewModal.vue";
import listOfReviewsForBook from "@/components/client/listOfReviewsForBook.vue";
</script>

<template>
    <ClientNavbar />
    <!-- {{ book }}
    {{ bookExists }} -->

    <div class="container p-3">
        <h1>Book Details</h1>
        <div v-if="book.error === 'Book not found'">
            <PageDoesNotExist />
        </div>
        <div v-else>
            <div class="container border rounded p-3">

                <div class="container d-flex justify-content-center p-5">
                    <img :src="getCoverURL(book.cover_path)" class="img-fluid" width="300px" height="400px">
                </div>
                <h3>{{ book.title }}</h3>
                <h5>Author: {{ book.author }}</h5>
                <h6>Section: {{ book.section }}</h6>
                <p>Description:</p>
                <p>{{ book.description }}</p>



                <div class="container d-flex col justify-content-left">
                    <div class="row">
                        <div class="d-flex justify-content-center">
                            <!-- Button trigger modal -->
                            <div class="container p-2">
                                <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                                    data-bs-target="#requestBookModal">
                                    Request Book
                                </button>
                            </div>
                            <!-- Modal -->
                            <div class="modal fade" id="requestBookModal" tabindex="-1" aria-labelledby="exampleModalLabel"
                                aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <form @submit="requestBook">
                                            <div class="modal-header">
                                                <h1 class="modal-title fs-5" id="exampleModalLabel">Modal title</h1>
                                                <button type="button" class="btn-close" data-bs-dismiss="modal"
                                                    aria-label="Close"></button>
                                            </div>
                                            <div class="modal-body">
                                                <h3>Enter Timing</h3>
                                                <div class="input-group mb-3">
                                                    <span class="input-group-text" id="basic-addon1">Days</span>
                                                    <input type="number" class="form-control" placeholder="Username"
                                                        aria-label="Username" aria-describedby="basic-addon1"
                                                        v-model="requestDays">
                                                </div>
                                                <div class="input-group mb-3">
                                                    <span class="input-group-text" id="basic-addon1">Hours</span>
                                                    <input type="number" class="form-control" placeholder="Username"
                                                        aria-label="Username" aria-describedby="basic-addon1"
                                                        v-model="requestHours">
                                                </div>
                                                <div class="input-group mb-3">
                                                    <span class="input-group-text" id="basic-addon1">Minutes</span>
                                                    <input type="number" class="form-control" placeholder="Username"
                                                        aria-label="Username" aria-describedby="basic-addon1"
                                                        v-model="requestMinutes">
                                                </div>
                                            </div>
                                            <div class="modal-footer">
                                                <button type="button" class="btn btn-secondary"
                                                    data-bs-dismiss="modal">Close</button>
                                                <button type="submit" class="btn btn-primary">Request</button>
                                            </div>
                                        </form>
                                        <div :class="msgclass" role="alert" v-if="msgstatus">
                                            {{ msg }}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="container p-2">
                            <CreateBookReviewModal />
                        </div>
                    </div>
                </div>
                <hr>
                <!-- {{ reviews }} -->
                <listOfReviewsForBook :reviews="reviews" />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            book: {},
            reviews: [],
            requested: false,
            bookExists: null,
            bookId: this.$route.params.id,

            requestDays: 1,
            requestHours: 0,
            requestMinutes: 0,

            msg: "",
            msgstatus: false,
            msgclass: ""


        }
    },
    methods: {
        getBookDetails() {

            fetch(store.getters.BASEURL + "/book/get/" + this.bookId, {
                method: "GET",
                headers: {
                    "Authentication-Token": store.getters.getToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.bookExists = true;
                    this.book = data;
                    console.log(this.book);
                })
                .catch(error => {
                    console.error("Error: ", error);;
                    this.bookExists = false;
                })
        },
        getCoverURL(value) {
            return `${store.getters.BASEURL}/static/covers/${value}`
        },
        requestBook(event) {
            event.preventDefault();
            console.log("Requesting book with id: ", this.book.id);
            fetch(store.getters.BASEURL + "/book/request", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken
                },
                body: JSON.stringify({
                    time: {
                        days: this.requestDays,
                        hours: this.requestHours,
                        minutes: this.requestMinutes
                    },
                    bookID: this.book.id,
                    userID: store.getters.getUserID
                }),
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    if (data.status == "success") {
                        console.log("Book requested successfully");
                        // alert("Book requested successfully");
                        this.requested = true;
                        this.msg = "Book requested successfully";
                        this.msgstatus = true;
                        this.msgclass = "alert alert-success"
                    }
                    else {
                        console.log("Error: ", data.error);
                        this.msg = "Error: " + data.error;
                        this.msgstatus = true;
                        this.msgclass = "alert alert-danger"
                    }
                })
        },
        getReviewsForBook(bookID) {
            fetch(store.getters.BASEURL + "/book/reviews/" + bookID, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    this.reviews = data;

                })
                .catch(error => {
                    console.error("Error: ", error);
                })

        }
    },
    created() {
        this.getBookDetails();
        this.getReviewsForBook(this.$route.params.id);
    }
}

</script>