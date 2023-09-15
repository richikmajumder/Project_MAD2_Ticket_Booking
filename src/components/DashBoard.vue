<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">
    <a class="navbar-brand" href="/">Ticketing App</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="/protected">Home</a>
        </li>
        <li class="nav-item">
          <router-link class="nav-link active" @click="booknow()" :to="{path:'/book'}">Book Tickets</router-link>
        </li>
        <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="#" @click="show('open')">Shows</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="#" @click="venue('open')">Venues</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="#" @click="stats('open')">Trending Shows</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" href="#" @click="MyWallet">
              Wallet <i class="bi bi-wallet"></i>
        </a>
          </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            My Account
          </a>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
            <li><a class="dropdown-item">Hello! <b>{{username}} </b> </a></li>
            <li><a class="dropdown-item" href="#" @click="bookinghistory('open')">Booking history</a></li>
            <li><a class="dropdown-item" href="#" @click="updateProfile('open')">My Profile</a></li> 
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#" @click="support('open')">Help & support</a></li>
            <li><a class="dropdown-item" href="#" @click="logout()">Sign out</a></li>
           
          </ul>
        </li>
        
      </ul>
      <form class="d-flex">
          <div class="search-container">
          <input  type="search" placeholder="Search" aria-label="Search" v-model="searchQuery" @input="handleSearchInput" @keyup.enter="performSearch" class="search-input">
      <ul v-if="showSuggestions" class="suggestions-list">
      <li v-for="suggestion in suggestions" :key="suggestion.id" @click="selectSuggestion(suggestion)">
        <span>{{ suggestion.result }}</span>
        <span class="suggestion-type">{{ suggestion.type }}</span>
      </li>
    </ul>
    
        </div>
          <!--button class="btn btn-outline-success" type="submit" v-on:click="alerting()">Search</button-->
        </form>
    </div>
  </div>
</nav>
<BookingHistory :username="username" v-if="history" @close="bookinghistory('close')"/>
    <div class="ms-5">
      <h1>User Dashboard</h1>
      <p>Email: {{ email }}</p>
      <p>Username: {{ username }}</p>
    </div>
<div class="child-center-container">
  <SearchResults :element="element" v-if="element" />
  <MyWallet :username="username" v-if="wallet" />
</div>
<HelpSupport v-if="help" @close="support('close')"></HelpSupport>
<ShowList :list="showlist" v-if="Show" v-on:close="show('close')" />
<VenueList :list="venuelist" v-if="Venue" v-on:close="venue('close')"/>
<UpdateProfile :username="username" v-if="UpdateProfile" v-on:close="updateProfile('close')"/>
<div class="child-center-container">
<VisualStats :name="'popular'" v-if="showstats"/>
</div>
  </template>
  
  <script>
  
  import BookingHistory from './BookingHistory.vue';
  import HelpSupport from './HelpSupport.vue';
  import ShowList from './ShowList.vue';
  import VenueList from './VenueList.vue';
  import SearchResults from './SearchResults.vue';
  import UpdateProfile from './UpdateProfile.vue';
  import MyWallet from './MyWallet.vue';
  import VisualStats from './VisualStats.vue';
  import { get } from '@/functions/get';
  import { url } from '@/functions/url';

  export default {
      name: 'DashBoard',
      components:{BookingHistory,HelpSupport,ShowList,VenueList,SearchResults,UpdateProfile,MyWallet,VisualStats},
    data() {
      return {
        email: '',
        username: '',
        history:false,
        help:false,
        Show:false,
        Venue:false,
        venuelist:null,
        showlist:null,
        searchQuery: '',
        suggestions: null,
        element: null,
        showSuggestions: false,
        UpdateProfile:false,
        wallet:false,
        showstats:false
      };
    },
    methods:{
      logout(){
        this.$store.commit('role',null)
        localStorage.removeItem('authToken');
        alert('Logged out successfully \n Redirecting to sign in page.')
        location.reload();
      },
        autoRefresh() {
        setTimeout(() => {
          location.reload();
        }, 1000);
      },
        booknow(){
          get(`${url}api/book`).then(data=>this.list=data)
        },
        bookinghistory(arg){
          if(arg==='open'){
            this.history=true
          }
          else if(arg==='close'){
            this.history=false
          }

        },
        support(arg){
          if(arg==='open'){
            this.help=true
          }
          else if(arg==='close'){
            this.help=false
          }
        },
        show(arg){
          if(arg==='open'){
            get(`${url}api/show`).then(data=>this.showlist=data)
            this.Show=true
          }
          else if(arg==='close'){
            this.Show=false
          }
        },
        venue(arg){
          if(arg==='open'){
            get(`${url}api/venue`).then(data=>this.venuelist=data)
            this.Venue=true
          }
          else if(arg==='close'){
            this.Venue=false
          }
        },
      async handleSearchInput() {
        if (this.searchQuery.length > 0) {
          if(this.showstats){
          this.showstats=false;
        }
        if(this.wallet){
        this.wallet=false;
        }
        await get(`${url}api/search?query=${this.searchQuery}`).then((data) => {
          this.suggestions = data;
        });
        this.suggestions.filter((suggestion) =>
          suggestion.result.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
        this.showSuggestions = true;
      } else {
        this.showSuggestions = false;
        this.suggestions = [];
      }
    },
    selectSuggestion(suggestion) {
      // Handle the selection of a suggestion
      // Replace the code below with your own logic
      console.log('Selected suggestion:', suggestion);
      this.searchQuery = suggestion.result;
      this.element = suggestion;
      this.showSuggestions = false;
    },
    performSearch() {
      // Handle the search operation
      // Replace the code below with your own logic
      console.log('Performing search:', this.searchQuery, this.element);
      // Clear the search query and hide suggestions
      this.searchQuery = '';
      this.showSuggestions = false;
    },
    updateProfile(arg){
      if(arg==='open'){
        this.UpdateProfile=true;
      }
      else if(arg==='close'){
        this.UpdateProfile=false;
      }
    },
    MyWallet(){
      this.element=null;
      this.showstats=false;
      this.wallet=true;

    },
    stats(arg){
      if(arg==='open'){
      this.showstats=true;
      this.element=null;
      this.wallet=false;
      }
      else if(arg==='close'){
        this.showstats=false
      }
    }


    },
    mounted() {
      // Get the auth_token from localStorage
      const authToken = localStorage.getItem('authToken');
      console.log(authToken)
      // Make an HTTP request to the protected route
      fetch(`${url}user/protected`, {
        headers: {
          Authorization: `Bearer ${authToken}`
        }
      })
      .then(response => {
        // Check if the response status is 200 (OK)
        if (response.ok) {
          this.$store.commit('role','user')
          return response.json();
        } else {
          //throw new Error('Unauthorized');
          this.$store.commit('role',null)
          localStorage.removeItem('authToken');
          this.$router.push('/signin');
          //alert('Logged out successfully \n Redirecting to sign in page.')
        }
      })
      .then(data => {
        // Update the email value with the email received from the server
        this.username = data.username;
        this.email = data.email;
      })
      .catch(error => {
        // Handle any errors or unauthorized access
        console.error(error);
  
        if (error.message === 'Unauthorized') {
          // Redirect to the login page or show an unauthorized message
          // Example: this.$router.push('/login');
        } else {
          // Show a generic error message
          // Example: this.errorMessage = 'An error occurred. Please try again.';
        }
      });
    },
    created(){
      //this.autoRefresh();
    }
  }
  </script>
  <style scoped>
  .modal{
display: flex;

}
  </style>
  