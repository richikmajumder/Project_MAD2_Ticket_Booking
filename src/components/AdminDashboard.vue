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
            <a class="nav-link active" aria-current="page" href="/admin/dashboard">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="#" @click="openshow('check')">Shows</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="#" @click="openvenue('check')">Venues</a>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Show Management
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><a class="dropdown-item" href="#" @click="openshow('add')">Add Show</a></li>
              <li><a class="dropdown-item" href="/modify/show">Modify Show</a></li>
              <li><a class="dropdown-item" href="#" @click.prevent="openshow('rem')">Remove Show</a></li>
              
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Venue Management
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><a class="dropdown-item" href="#" @click="openAddvenue">Add Venue</a></li>
              <li><a class="dropdown-item" href="/modify/venue">Modify Venue</a></li>
              <li><a class="dropdown-item" href="#" @click.prevent="openvenue('rem')">Remove Venue</a></li>
              <li><a class="dropdown-item" aria-current="page" href="#" @click="exportvenue('open')">Export Venue</a></li>
              
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Stats
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><a class="dropdown-item" href="#" @click="stats('show')" >Show Stats</a></li>
              <li><a class="dropdown-item" href="#" @click="stats('venue')" >Venue Stats</a></li>
            </ul>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              My Account
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
              <li><a class="dropdown-item">Hello! <b>{{ username }}</b></a></li>
              <li><a class="dropdown-item" href="#" @click="updateProfile('open')">Update Profile</a></li>
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

  <AddShow :list="venuelist" v-if="addShow" v-on:close="closeAddshow" @submitData="addShowfn"/>
  <ShowList :list="showlist" v-if="Show" v-on:close="closeshow('add')" />
  <AddVenue v-if="addVenue" v-on:close="closeAddvenue" @submitData="addVenuefn"/>
  <VenueList :list="venuelist" v-if="Venue" v-on:close="closevenue('check')"/>
  <RemoveVenue :list="venuelist" v-if="VenueRemoval" v-on:close="closevenue('rem')" @Remove="erasevenue"/>
  <RemoveShow :list="showlist" v-if="ShowRemoval" v-on:close="closeshow('rem')" @Remove="eraseshow"/>
  <HelpSupport v-if="help" @close="support('close')"/>
  <ExportVenue :list="venuelist" :username="username" v-if="Export" v-on:close="exportvenue('close')"/>
  <UpdateProfile :username="username" v-if="UpdateProfile" v-on:close="updateProfile('close')"/>
  <div class="ms-5">
    <h1>Admin Dashboard</h1>
    <p>Email: {{ email }}</p>
    <p>Username: {{ username }}</p>
    
  </div>
  <div class="child-center-container">
  <SearchResults :element="element" v-if="element" />
</div>
<div class="child-center-container">
  <VisualStats :name="Stats" v-if="Stats"/>
</div>
</template>

    
    <script>
    import '../style.css'
    import alertify from 'alertifyjs';
    import AddShow from './AddShow.vue';
    import ShowList from './ShowList.vue';
    import AddVenue from './AddVenue.vue';
    import VenueList from './VenueList.vue';
    import RemoveVenue from './RemoveVenue.vue';
    import RemoveShow from './RemoveShow.vue';
    import HelpSupport from './HelpSupport.vue';
    import ExportVenue from './ExportVenue.vue';
    import VisualStats from './VisualStats.vue';
    import SearchResults from './SearchResults.vue';
    import UpdateProfile from './UpdateProfile.vue';
    import { update } from '../functions/update.js';
    import { remove } from '../functions/remove.js';
    import { get } from '@/functions/get.js';
    import { cache_get } from '@/functions/cache_get.js'
    import { url } from '@/functions/url.js';
    

    export default {
        name: 'AdminDashboard',
        components:{AddShow,ShowList,AddVenue,VenueList,RemoveVenue,RemoveShow,HelpSupport,ExportVenue,SearchResults,UpdateProfile,VisualStats},
      data() {
        return {
          email: '',
          username: '',
          addShow: false,
          addVenue: false,
          Show:false,
          Venue: false,
          VenueRemoval: false,
          ShowRemoval: false,
          showname:'',
          rating:null,
          tags:'',
          place:'',
          location:'',
          capacity:null,
          venuelist:null,
          showlist:null,
          help:false,
          Export:false,
          searchQuery: '',
          suggestions: null,
          element: null,
          showSuggestions: false,
          UpdateProfile:false,
          Stats:null
        };
      },
methods:{
    logout(){
          localStorage.removeItem('authToken');
          this.$store.commit('role',null)
          alert('Logged out successfully \n Redirecting to sign in page.')
          location.reload();
        },
    openAddshow() {
      this.addShow = true;
    },
    closeAddshow() {
      this.addShow = false;
    },
    openshow(arg){
      if(arg==='add'){
        get(`${url}api/venue`).then(data=>this.venuelist=data)
        this.openAddshow()
      }
      else if(arg==='check'){
        get(`${url}api/show`).then(data=>this.showlist=data)
        console.log(this.showlist)
        this.Show = true;
        
      }
      else if(arg==='rem'){
        cache_get(`${url}api/show`).then(data=>this.showlist=data)
        this.ShowRemoval = true;
      }
    },

    closeshow(arg){
      if(arg==='add'){
        this.Show = false;
      }
      else if(arg==='rem'){
        this.ShowRemoval = false;
      }
    },

    async eraseshow(data){
      console.log(data);
      await remove(`${url}api/show/delete/${data.id}`);
      this.openshow('rem')},

    addShowfn(data){
      this.showname=data.name,
      this.rating=data.rating,
      this.tags=data.tags;
      //const payload = {showname:this.showname,rating:this.rating,tags:this.tags,venue_id:this.venue_id,venue_name:this.venue_name,venue_place:this.venue_place,venue_location:this.venue_location}
      alertify.alert(`Show name : ${this.showname}, Show rating: ${this.rating}, Show tags: ${this.tags} added succesfully`)
      //this.closeAddshow()
      //location.reload()
      update(`${url}api/show`,data,this.$router);
      console.log(data);
      this.closeAddshow();
    },
    openAddvenue(){
      this.addVenue=true;
    },
    closeAddvenue(){
      this.addVenue=false;
    },
    openvenue(arg){
      if(arg==='rem'){
        cache_get(`${url}api/venue`).then(data=>this.venuelist=data);
        this.VenueRemoval=true;
      }
      else if(arg==='check'){
        get(`${url}api/venue`).then(data=>this.venuelist=data);
        this.Venue=true;
      }
      
    },
    closevenue(arg){
      if(arg==='check'){
      this.Venue=false;
      }
      else if(arg==='rem'){
        this.VenueRemoval=false;
      }
    },
    addVenuefn(data){
      this.venuename=data.name;
      this.place=data.place;
      this.location=data.location;
      this.capacity=data.capacity;
      const payload = {venuename:this.venuename,place:this.place,location:this.location,capacity:this.capacity}
      //alertify.alert(`${this.venuename},${this.place},${this.location},${this.capacity}`);
      this.closeAddvenue();
      //location.reload()
      update(`${url}api/venue`,payload,this.$router)
    },
    async erasevenue(data){
      //this.closevenue('rem');
      console.log(data);
      //this.closevenue('rem')
      await remove(`${url}api/venue/delete/${data.id}`);
      //location.reload();
      this.openvenue('rem');
    },

    support(arg){
          if(arg==='open'){
            this.help=true
          }
          else if(arg==='close'){
            this.help=false
          }
        },
    exportvenue(arg){
          if(arg==='open'){
            get(`${url}api/venue`).then(data=>this.venuelist=data)
            this.Export=true
          }
          else if(arg==='close'){
            this.Export=false
          }
        },

    async handleSearchInput() {
      if (this.searchQuery.length > 0) {
        if(this.Stats){
          this.Stats=false;
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
    stats(arg){
      
      if(arg==='show'){
        if(this.element!=null){
          this.element=null
        }
        this.Stats='show';
      }
      else if(arg==='venue'){
        if(this.element!=null){
          this.element=null
        }
        this.Stats='venue';
      }
    }

    
},
mounted() {
        // Get the auth_token from localStorage
        const authToken = localStorage.getItem('authToken');
        console.log(authToken)
        // Make an HTTP request to the protected route
        fetch(`${url}protected`, {
          headers: {
            Authorization: `Bearer ${authToken}`
          }
        })
        .then(response => {
          // Check if the response status is 200 (OK)
          if (response.ok) {
            this.$store.commit('role','admin')
            return response.json();
          } else {
            //throw new Error('Unauthorized');
            localStorage.removeItem('authToken');
            this.$store.commit('role',null);
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
    }
    </script>

<style scoped>
.modal{
display:flex;

}
</style>
    