import { createRouter, createWebHistory } from 'vue-router'
import SignInView from '../views/SignInView.vue'
import HomeView from '../views/HomeView.vue'
import SignUpView from '../views/SignUpView.vue'
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import BookSectionsView from '@/views/admin/BookSectionsView.vue'
import store from '@/store'
import UnauthorizedAccess from '@/components/UnauthorizedAccess.vue'
import BooksView from '@/views/admin/BooksView.vue'
import CreateBookEntry from '@/views/admin/CreateBookEntry.vue'
import BookDescriptionView from '@/views/BookDescriptionView.vue'
import BookRequests from '@/components/admin/BookRequests.vue'
import UserBookRequestsView from '@/views/client/UserBookRequestsView.vue'
import UserBookIssuesView from '@/views/client/UserBookIssuesView.vue'
import AdminBookIssuesView from '@/views/admin/AdminBookIssuesView.vue'
import UserReviewsView from '@/views/client/UserReviewsView.vue'
import AdminReviewsView from '@/views/admin/AdminReviewsView.vue'
import AdminHomeStats from '@/components/admin/AdminHomeStats.vue'
import UserProfileView from '@/views/client/UserProfileView.vue'
import myBooksView from '@/views/myBooksView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/signin',
      name: 'signin',
      component: SignInView
    },
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminDashboard,
      children: [
        {
          path: '',
          name: 'admin-home',
          component: AdminHomeStats
        },
        {
          path: 'sections',
          name: 'sections',
          component: BookSectionsView
        },
        {
          path: 'books',
          name: 'books',
          component: BooksView
        },
        {
          path: 'book/create',
          name: 'book-create',
          component: CreateBookEntry
        },
        {
          path: 'book/requests',
          name: 'book-requests',
          component: BookRequests
        },
        {
          path: 'book/issues',
          name: 'book-issues',
          component: AdminBookIssuesView
        },
        {
          path: 'reviews',
          name: 'reviews',
          component: AdminReviewsView
        }
        // {
        //   path: 'book/edit/:id',
        //   name: 'book/edit',
        //   component: UpdateBookEntry
        // }
      ]
    },
    {
      path: '/book/:id',
      name: 'book',
      component: BookDescriptionView
    },
    {
      path: '/mybooks',
      name: 'myBooks',
      component: myBooksView
    },
    {
      path: '/mybookrequests',
      name: 'my-book-requests',
      component: UserBookRequestsView
    },
    {
      path: '/mybookissues',
      name: 'my-book-issues',
      component: UserBookIssuesView
    },
    {
      path: '/myreviews',
      name: 'my-reviews',
      component: UserReviewsView
    },
    {
      path: '/myprofile',
      name: 'my-profile',
      component: UserProfileView
    },
    {
      path: '/unauthorized',
      name: 'unauthorized',
      component: UnauthorizedAccess
    }
  ]
})

router.beforeEach((to) => {
  // redirects for me being stupid
  if (to.path === '/login') {
    return { name: 'signin' }
  }

  // actually useful redirects
  if (to.path === '/' && store.getters.getRoles.includes('admin') && store.getters.getToken) {
    console.log('getRoles function return value: ', store.getters.getRoles.includes('admin'))
    return { path: '/admin' }
  }

  if (to.path === '/' && !store.getters.getToken) {
    console.log('no token')
    return { name: 'signin' }
  }

  // add admin side links are only accessible to users with admin role
  if (
    to.path.match('/admin*') &&
    !store.getters.getRoles.includes('admin') &&
    store.getters.getToken != null
  ) {
    console.log('no admin role')
    return { name: 'unauthorized' }
  }
})

export default router
