<script setup>
import store from "@/store";

</script>

<template>
    <!-- Button trigger modal -->
    <button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#updateSectionModal">
        Update Section
    </button>

    <!-- Modal -->
    <div class="modal fade" id="updateSectionModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Modal title</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form @submit="updateSection">
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="section" class="form-label">Section Name</label>
                            <input type="text" class="form-control" id="section" aria-describedby="sectionHelp"
                                v-model="newsectionName">
                            <div id=" sectionHelp" class="form-text">Mandatory
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="description" class="form-label">Description</label>
                            <textarea class="form-control" id="description" rows="3" v-model="newsectionDesc"></textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary">Update Section</button>
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
    props: ["currentSection"],
    data() {
        return {
            newsectionName: this.currentSection.name,
            newsectionDesc: this.currentSection.description,

            errstatus: false,
            msg: "",
            errclass: "",

            componentKey: 0,

        }
    },
    methods: {
        validate() {
            if (this.newsectionName == "") {
                this.errstatus = true;
                this.msg = "Section Name is mandatory";
                this.errclass = "alert alert-danger";
                return false;
            }
            if (this.newsectionName.length < 3) {
                this.errstatus = true;
                this.msg = "Section Name should be atleast 3 characters long";
                this.errclass = "alert alert-danger";
                return false;
            }
            return true;
        },

        updateSection(event) {
            event.preventDefault()
            if (this.validate()) {
                console.log("Frontend Update Section Validation Successful.")
                console.log("Section Name: ", this.newsectionName, "Description: ", this.newsectionDesc)
                fetch(store.getters.BASEURL + "/admin/section/update" + "/" + this.currentSection.id, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authentication-Token": store.getters.getToken
                    },
                    body: JSON.stringify({
                        sectionName: this.newsectionName,
                        sectionDesc: this.newsectionDesc,
                    }),
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data)
                        if (data.status == "success") {
                            this.errstatus = true;
                            this.msg = "Section Updated Successfully";
                            this.errclass = "alert alert-success";
                            // reload the page
                            window.location.reload();


                        } else {
                            this.errstatus = true;
                            this.msg = data.error;
                            this.errclass = "alert alert-danger";
                        }
                    })
            }
        },
    }
}
</script>