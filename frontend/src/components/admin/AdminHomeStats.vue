<script setup>
import store from "@/store";
</script>


<template>
    {{ }}

    <!-- {{ sectionsPieChartData }} -->

    {{ barChartseries }}
    <div class="container-fluid d-flex row align-items-center">
        <div class="col">
            <h1>eLib Admin Dashboard</h1>
            <div class="container p-5">
                <h5>Total Requests: {{ this.total_requests }}</h5>
                <hr>
                <h5>Total Active Issues: {{ this.total_issues }}</h5>
                <hr>
                <h5>Overdue Issues: {{ this.overdue_issues }}</h5>
            </div>
            <apexchart type="pie" :options="optionSections" :series="sectionsPieChartData.counts" />
            <br>
        </div>
        <div class="col">
            <apexchart max-width="600" type="bar" :options="optionRequests"
                :series="topRequestedBooksBarChartData.counts" />
            <apexchart max-width="600" type="bar" :options="optionTopRated" :series="toppRatedBooksBarChartData.rating" />
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            stats: {},
            sectionsPieChartData: {
                books: [],
                counts: []
            },
            topRequestedBooksBarChartData: {
                books: [],
                counts: []
            },
            toppRatedBooksBarChartData: {
                books: [],
                rating: []
            },
            total_requests: 0,
            total_issues: 0,
            overdue_issues: 0,

        }
    },
    methods: {
        getAdminStats() {
            fetch(store.getters.BASEURL + "/admin/dashboard/get_data", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": store.getters.getToken
                }
            })
                .then(response => response.json())
                .then(data => {
                    this.stats = data;
                    // this.booksoriginal = data;
                    // this.transformData(this.sections)
                    this.sectionsPieChartData.books = data[0].book_count_by_section.books
                    this.sectionsPieChartData.counts = data[0].book_count_by_section.counts

                    this.topRequestedBooksBarChartData.books = data[1].top_requested_books.books
                    this.topRequestedBooksBarChartData.counts = data[1].top_requested_books.counts

                    this.toppRatedBooksBarChartData.books = data[2].top_rated_books.books
                    this.toppRatedBooksBarChartData.rating = data[2].top_rated_books.rating

                    this.total_requests = data[3].total_requests
                    this.total_issues = data[4].total_issues
                    this.overdue_issues = data[5].overdue_issues
                })
                .catch(error => {
                    console.error("Error: ", error);
                })
        }
    },
    computed: {
        optionSections() {
            return {
                chart: {
                    type: 'donut'
                },
                title: {
                    text: 'Section Wise Book Count'
                },
                series: [{
                    data: this.sectionsPieChartData.counts,
                }],
                labels: this.sectionsPieChartData.books,
            }
        },
        optionRequests() {
            return {
                chart: {
                    type: 'bar'
                },
                title: {
                    text: 'Top Requested Books'
                },
                series: [{
                    data: this.topRequestedBooksBarChartData.counts,
                }],
                xaxis: {
                    categories: this.topRequestedBooksBarChartData.books,
                },
                height: 100
            }
        },
        optionTopRated() {
            return {
                chart: {
                    type: 'bar'
                },
                title: {
                    text: 'Top Rated Books'
                },
                series: [{
                    data: this.toppRatedBooksBarChartData.rating,
                }],
                xaxis: {
                    categories: this.toppRatedBooksBarChartData.books,
                },
                height: 100
            }
        }
    },
    created() {
        this.getAdminStats()
    }
}
</script>