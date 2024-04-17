<template>
    <div class="container-fluid">
        <div class="container-fluid rounded p-3">
            <div class="row">

                <div class="col-sm-6 mb-3 mb-sm-0">
                    <div class="card" width="70%" :class="review.rating < 5 ? 'border-danger' : 'border-success'">
                        <div class="card-body">
                            <h5 class="card-title">{{ review.review_title }}</h5>
                            <div class="d-flex col justify-content-start">
                                <div class="row p-2">
                                    <p class="card-text">{{ review.user }}</p>
                                </div>
                                <div class="row p-2">
                                    <div class="text-muted">|</div>
                                </div>
                                <div class="row p-2">
                                    <p class="card-text">{{ review.rating }}/10</p>
                                </div>
                            </div>
                            <p class="card-text"><small class="text-muted">{{ review.review_date }}</small></p>
                            <hr>
                            <p class="card-text">{{ review.review_desc }}.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ['review'],
    data() {
        return {
            borderClass: ""
        }
    },
    methods: {

    }
}
</script>