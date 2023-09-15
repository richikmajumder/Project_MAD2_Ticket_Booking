import { createRouter, createWebHistory } from 'vue-router'
//import HomeView from '../views/HomeView.vue'
import HomePage from '../components/HomePage.vue'
import SignIn from '../components/SignIn.vue'
import SignUp from '../components/SignUp.vue'
import DashBoard from '../components/DashBoard.vue'
import ModifyVenue from '../components/ModifyVenue.vue'
import ModifyShow from '../components/ModifyShow.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import ShowDetails from '../components/ShowDetails.vue'
import VenueDetails from '../components/VenueDetails.vue'
import ShowLink from '../components/ShowLink.vue'
import VenueLink from '../components/VenueLink.vue'
import BookNow from '../components/BookNow.vue'
import BookingConfirmation from '../components/BookingConfirmation.vue'
import ForgotPassword from '../components/ForgotPassword.vue'
import ResetPassword from '../components/ResetPassword.vue'
import ErrorPage from '../components/ErrorPage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/signin',
    name: 'signin',
    component: SignIn
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignUp,
    meta : {isadmin:false}
  },
  {
    path: '/protected',
    name: 'DashBoard',
    component: DashBoard
  },
  {
    path: '/modify/venue',
    name: 'ModifyVenue',
    component: ModifyVenue
  },
  {
    path: '/modify/show',
    name: 'ModifyShow',
    component: ModifyShow
  },
  {
    path: '/admin/signup',
    name: 'AdminSignup',
    component: SignUp,
    meta : {isadmin:true}
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard
  },
  {
    path: '/show/details/:id',
    name: 'ShowDetails',
    component: ShowDetails
  },
  { 
    path: '/venue/details/:id',
    name: 'VenueDetails',
    component: VenueDetails
  },
  {
    path: '/admin/venuelink/:id',
    name: 'VenueLink',
    component: VenueLink
  },
  {
    path: '/admin/showlink/:id',
    name: 'ShowLink',
    component: ShowLink
  },
  {
    path: '/book',
    name: 'BookNow',
    component: BookNow
  },
  {
    path: '/book/:id',
    name: 'BookingConfirmation',
    component: BookingConfirmation
  },
  {
    path: '/forgot/password',
    name: 'ForgotPassword',
    component: ForgotPassword
  },
  {
    path: '/api/reset/password/:token',
    name: 'ResetPassword',
    component: ResetPassword
  },
  {
    path:'/:catchAll(.*)',
    name: 'ErrorPage',
    component: ErrorPage
  }
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
