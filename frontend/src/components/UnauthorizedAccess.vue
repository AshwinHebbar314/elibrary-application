<script setup>
import ClientNavbar from "@/components/ClientNavbar.vue";
</script>

<template>
    <ClientNavbar />
    <div class="container centered">
        <div class="alert alert-danger" role="alert">
            <h4 class="alert-heading">Unauthorized</h4>
            <p>This account is not authorize to access this end point.</p>
            <hr>
            <p class="mb-0">Think there's a mistake? Contact the librarian for more info.</p>
        </div>
    </div>
</template>

