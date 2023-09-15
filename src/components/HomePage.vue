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
            <a class="nav-link active" aria-current="page" href="/">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="#" @click="show('open')">Shows</a>
          </li>
          <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="#" @click="venue('open')">Venues</a>
          </li>
          <li class="nav-item" v-if="role!='admin'">
            <a class="nav-link" href="/book">Book Tickets</a>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              My Account
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown" v-if="role===null">
              <li><a class="dropdown-item" href="/signup">Sign up</a></li>
              <li><a class="dropdown-item" href="/signin">Sign in</a></li>
            </ul>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown" v-if="role==='user'">
              <li><a class="dropdown-item" href="/protected">Dashboard</a></li>
              <li><a class="dropdown-item" href="#" @click="logout">Log out</a></li>
            </ul>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown" v-if="role==='admin'">
              <li><a class="dropdown-item" href="/admin/dashboard">Admin Dashboard</a></li>
              <li><a class="dropdown-item" href="#" @click="logout">Log out</a></li>
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
  <div class="child-center-container">
  <SearchResults :element="element" v-if="element" />
</div>
<ShowList :list="showlist" v-if="Show" v-on:close="show('close')" />
<VenueList :list="venuelist" v-if="Venue" v-on:close="venue('close')"/>
</template>

<script>
import { get } from '@/functions/get';
import SearchResults from './SearchResults.vue'; // Import the child component
import ShowList from './ShowList.vue';
import VenueList from './VenueList.vue';
import { url } from '@/functions/url';

export default {
  name: 'HomePage',
  components: {
    SearchResults,ShowList,VenueList // Register the child component
  },
  data() {
    return {
      searchQuery: '',
      suggestions: null,
      element: null,
      showSuggestions: false,
      venuelist:null,
      showlist:null,
      Show:false,
      Venue:false,
      role:null
    };
  },
  mounted(){
  fetch(`${url}api/token/verifier`,{
            headers: {
            Authorization: `Bearer ${localStorage.getItem('authToken')}`
          },
        }).then(response => {
          // Check if the response status is 200 (OK)
          if (response.ok) {
            return response.json();
          }
          else{
              console.log(response.statusText)
              console.timeLog(response.json().message)
          }}).then(data=>this.role=data.role).catch(error=>console.log(error))
  },
  methods: {
    async handleSearchInput() {
      if (this.searchQuery.length > 0) {
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
    logout(){
        this.$store.commit('role',null)
        this.role=null
        localStorage.removeItem('authToken');
        alert('Logged out successfully')
        location.reload();
      }
  },
  watch:{
    role(newValue,oldValue){
      console.log(oldValue,newValue)
      if(newValue==='admin'){
      this.$store.commit('role','admin')}
      else if(newValue==='user'){
        this.$store.commit('role','user')
      }
      else{
        this.$store.commit('role',null)
      }
    }}
  }
</script>

<style scoped>
.modal{
display: flex;

}
.home{
  background-color: #D1C4E9;
}

</style>
