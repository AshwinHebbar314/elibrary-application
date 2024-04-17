<script setup>
import CreateSectionModal from '@/components/CreateSectionModal.vue';
import ListSection from '@/components/ListSection.vue';
</script>

<template>
    <div class="container">
        <ListSection />
    </div>
    <div class="container p-3">
        <CreateSectionModal />
    </div>
</template>

<script>
export default {
    data() {
        return {
            // sectionName: "",
            // sectionDesc: "",

            // errstatus: false,
            // output: "",
            // bsclass: "alert alert-danger"
        }
    },
    methods: {

    }
}
</script>