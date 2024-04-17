<script setup>
import store from "@/store";

</script>

<template>
    <!-- Button trigger modal -->
    <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createSectionModal">
        Add a new Section
    </button>

    <!-- Modal -->
    <div class="modal fade" id="createSectionModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Modal title</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <form @submit="createSection">
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="section" class="form-label">Section Name</label>
                            <input type="text" class="form-control" id="section" aria-describedby="sectionHelp"
                                v-model="sectionName">
                            <div id="sectionHelp" class="form-text">Mandatory</div>
                        </div>
                        <div class="mb-3">
                            <label for="description" class="form-label">Description</label>
                            <textarea class="form-control" id="description" rows="3" v-model="sectionDesc"></textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="submit" class="btn btn-primary">Create Section</button>
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
    data() {
        return {
            sectionName: "",
            sectionDesc: "",

            errstatus: false,
            msg: "",
            errclass: "",

            componentKey: 0,
        }
    },
    methods: {
        validate() {
            if (this.sectionName == "") {
                this.errstatus = true;
                this.msg = "Section Name is mandatory";
                this.errclass = "alert alert-danger";
                return false;
            }
            if (this.sectionName.length < 3) {
                this.errstatus = true;
                this.msg = "Section Name should be atleast 3 characters long";
                this.errclass = "alert alert-danger";
                return false;
            }
            return true;
        },

        createSection(event) {
            event.preventDefault()
            if (this.validate()) {
                console.log("Frontend Create Section Validation Successful.")
                console.log("Section Name: ", this.sectionName, "Description: ", this.sectionDesc)
                fetch(store.getters.BASEURL + "/admin/section/create", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authentication-Token": store.getters.getToken
                    },
                    body: JSON.stringify({
                        sectionName: this.sectionName,
                        sectionDesc: this.sectionDesc,
                    }),
                })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data)
                        if (data.status == "success") {
                            this.errstatus = true;
                            this.msg = "Section Created Successfully";
                            this.errclass = "alert alert-success";

                            // reload the page, !NOT IDEAL, BUT WORKS
                            window.location.reload()


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