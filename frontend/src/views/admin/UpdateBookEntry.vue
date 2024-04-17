<script setup>
import store from '@/store';
</script>

<template>
    <!-- Button trigger modal -->
    <button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#updateBookEntryModal">
        Update
    </button>

    <!-- Modal -->
    <div class="modal modal-xl fade" id="updateBookEntryModal" tabindex="-1" aria-labelledby="exampleModalLabel"
        aria-hidden="true">
        <div class="modal-dialog centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Modal title</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form @submit="updateBook">
                    <div class="p-3 centered-page-top">
                        <h1>Update a Book</h1>
                    </div>
                    <div class="container border rounded">
                        <div class="p-3">
                            <div class="mb-3">
                                <label for="title" class="form-label">Title</label>
                                <input type="text" class="form-control" id="title" aria-describedby="titleHelp"
                                    v-model="title">
                                <div id="titleHelp" class="form-text">Mandatory</div>
                            </div>
                            <div class="mb-3">
                                <label for="description" class="form-label">Description</label>
                                <textarea class="form-control" id="description" rows="3" v-model="description"></textarea>
                            </div>
                            <div class="d-flex mb-3 row ">
                                <div class="col">
                                    <label class="form-label">Author first name</label>
                                    <input type="text" class="form-control" id="authorFirstName"
                                        aria-describedby="authorFirstNameHelp" v-model="authorFirstName">
                                    <div class="form-text" id="fnameHelp">Mandatory</div>
                                </div>
                                <div class="col">
                                    <label class="form-label">Author last name</label>
                                    <input type="text" class="form-control" id="authorLastName"
                                        aria-describedby="authorLastNameHelp" v-model="authorLastName">
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="section" class="form-label">Section</label>
                                <select class="form-select" id="section" v-model="section">
                                    <option v-for="section in sections" :key="section.id" :value="section.id">{{
                                        section.name }}
                                    </option>
                                </select>
                            </div>
                            <div class="d-flex mb-3 row">
                                <div class="col">
                                    <label for="bookCover" class="form-label">Book Cover</label>
                                    <input type="file" class="form-control" id="bookCover" aria-describedby="bookCoverHelp"
                                        @change="getCover" accept=".jpg,.png">
                                </div>
                                <div class="col">
                                    <label for="bookFile" class="form-label">Book File</label>
                                    <input type="file" class="form-control" id="bookFile" aria-describedby="bookFileHelp"
                                        @change="getFile" accept=".pdf">
                                </div>
                            </div>
                            <div class="d-flex justify-content-center">
                                <button type="submit" class="btn btn-primary">Update Book</button>
                            </div>
                        </div>
                    </div>
                </form>
                <div :class="errclass" role="alert" v-if="errstatus">
                    {{ msg }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ["currentBook"],
    data() {
        return {
            title: this.currentBook.title,
            description: this.currentBook.description,
            authorFirstName: this.currentBook.author_fname,
            authorLastName: this.currentBook.author_lname,
            section: this.currentBook.section,
            bookCover: null,
            bookCover2: null,
            bookFile: null,
            bookFile2: null,
            sections: [],

            msg: "",
            errstatus: false,
            errclass: ""
        }
    },
    methods: {
        getCover(event) {
            this.bookCover = event.target.files[0];
            this.readCover();
        },
        getFile(event) {
            this.bookFile = event.target.files[0];
            this.readFile();
        },
        readCover() {
            const reader = new FileReader();
            reader.addEventListener('load', (event) => {
                this.bookCover2 = event.target.result;
            });
            reader.readAsDataURL(this.bookCover);
        },
        readFile() {
            const reader = new FileReader();
            reader.addEventListener('load', (event) => {
                this.bookFile2 = event.target.result;
            });
            reader.readAsDataURL(this.bookFile);
        },
        validate() {
            // if title is less than 3 characters
            if (this.title.length < 3) {
                this.errstatus = true;
                this.msg = "Title should be atleast 3 characters long";
                this.errclass = "alert alert-danger";
                return false;
            }
            if (this.authorFirstName == "") {
                this.errstatus = true;
                this.msg = "Author First Name is mandatory";
                this.errclass = "alert alert-danger";
                return false;
            }
            return true;
        },
        updateBook(event) {
            event.preventDefault();
            if (this.validate()) {
                console.log("Frontend Book Validation Successful.")
                console.log("Title: ", this.title, "Description: ", this.description, "Author First Name: ", this.authorFirstName, "Author Last Name: ", this.authorLastName, "Section: ", this.section, "Book Cover: ", this.bookCover, "Book File: ", this.bookFile)
                let form = new FormData();
                form.append("title", this.title);
                form.append("description", this.description);
                form.append("authorFirstName", this.authorFirstName);
                form.append("authorLastName", this.authorLastName);
                form.append("section", this.section);
                form.append("bookCover", this.bookCover);
                form.append("bookFile", this.bookFile);


                fetch(store.getters.BASEURL + "/admin/book/update" + "/" + this.currentBook.id, {
                    method: "PUT",
                    headers: {
                        "Authentication-Token": store.getters.getToken
                    },
                    body: form
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        if (data.status == "success") {
                            console.log("Book updated successfully");
                            this.bsclass = "alert alert-success";
                            this.title = "";
                            this.description = "";
                            this.authorFirstName = "";
                            this.authorLastName = "";
                            this.section = "";
                            this.bookCover = null;
                            this.bookCover2 = null;
                            this.bookFile = null;
                            this.bookFile2 = null;
                        }
                        else {
                            alert("Error: " + data.message);
                        }
                    }).catch(error => {
                        console.error("Error: ", error);
                    });
            }
        },
        getSections() {
            fetch(store.getters.BASEURL + "/admin/section/getList", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.sections = data;
                })
                .catch(error => {
                    console.error("Error: ", error);
                });
        }
    },
    mounted() {
        this.getSections();
        console.log("Sections: ", this.sections);
    }
}
</script>