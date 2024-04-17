<script setup>
import store from "@/store";
</script>

<template>
    <div class="container p-3">
        <h1>Book Requests</h1>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Request ID</th>
                    <th>Book Title</th>
                    <th>Requested By</th>
                    <th>Requested On</th>
                    <th>Requested for</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="bookRequest in bookRequests" :key="bookRequest.id">
                    <td>{{ bookRequest.id }}</td>
                    <td>{{ bookRequest.bookTitle }}</td>
                    <td>{{ bookRequest.userName }}</td>
                    <td>{{ bookRequest.request_date }}</td>
                    <td>{{ secondsToDhms(bookRequest.request_duration) }}</td>
                    <td v-if="bookRequest.request_status === 'pending'">
                        <button class="btn btn-success p-2"
                            @click="processBookRequest(bookRequest.id, 'approved')">Approve</button>
                        <button class="btn btn-danger p-2"
                            @click="processBookRequest(bookRequest.id, 'rejected')">Reject</button>
                    </td>
                    <td v-else>
                        {{ bookRequest.request_status }}
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    data() {
        return {
            bookRequests: [],
            bookRequestOriginal: [],
            process: null
        }
    },
    methods: {
        fetchBookRequests() {
            console.log("Fetching book requests");
            fetch(store.getters.BASEURL + "/admin/book/request/getList", {
                method: "GET",
                headers: {
                    // "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.bookRequests = data;
                    this.bookRequestOriginal = data;
                })
                .catch(error => {
                    console.error("Error: ", error);
                })
        },
        secondsToDhms(seconds) {
            seconds = Number(seconds);
            var d = Math.floor(seconds / (3600 * 24));
            var h = Math.floor(seconds % (3600 * 24) / 3600);
            var m = Math.floor(seconds % 3600 / 60);
            var s = Math.floor(seconds % 60);

            var dDisplay = d > 0 ? d + (d == 1 ? " d " : " d ") : "";
            var hDisplay = h > 0 ? h + (h == 1 ? " h " : " h ") : "";
            var mDisplay = m > 0 ? m + (m == 1 ? " m " : " m ") : "";
            var sDisplay = s > 0 ? s + (s == 1 ? " s " : " s ") : "";
            return dDisplay + hDisplay + mDisplay + sDisplay;
        },
        processBookRequest(requestID, status) {
            console.log("Approving book request with id: ", requestID);
            fetch(store.getters.BASEURL + "/admin/book/request/process" + "/" + requestID, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken
                },
                body: JSON.stringify({
                    status: status
                })
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data);
                    if (data.status == "success") {
                        this.fetchBookRequests();
                    }
                })
                .catch(error => {
                    console.error("Error: ", error);
                });
        },
    },
    created() {
        this.fetchBookRequests();
    }
}

</script>