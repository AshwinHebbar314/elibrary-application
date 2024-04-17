<script setup>
import store from "@/store"
import UpdateSectionModal from "./UpdateSectionModal.vue";
</script>

<template>
    <div class="container p-3">
        <h1>Sections</h1>
        <ul>
            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th>id</th>
                        <th>Section Name</th>
                        <!-- <th>Description</th> -->
                        <th>Date Created</th>
                        <th>Delete</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="section in  sections " :key="section.id">
                        <td>{{ section.id }}</td>
                        <td>{{ section.name }}</td>
                        <td>{{ Date(section.dateCreated) }}</td>
                        <td>
                            <button class="btn btn-danger" @click="deleteSection(section.id)">Delete</button>
                        </td>
                        <!-- {{ section }} -->
                        <td>
                            <UpdateSectionModal :currentSection="section" />
                        </td>
                    </tr>
                </tbody>
            </table>
        </ul>
    </div>
</template>

<script>
export default {
    data() {
        return {
            sections: []

        }
    },
    methods: {
        fetchSections() {
            console.log("Fetching sections");
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
                    // this.transformData(this.sections)
                })
                .catch(error => {
                    console.error("Error: ", error);
                });
        },
        deleteSection(sectionID) {
            console.log("Deleting section with id: ", sectionID)
            fetch(store.getters.BASEURL + "/admin/section/delete/" + sectionID, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken,
                    'Access-Control-Allow-Origin': "*"
                },

            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    if (data.status == "success") {
                        console.log("Section deleted successfully");
                        this.fetchSections();
                    }
                    else {
                        alert("Error: " + data.error);
                    }
                })
                .catch(error => {
                    console.error("Error: ", error);
                });
        },
    },
    created() {
        this.sections = this.fetchSections();
    },
}

</script>