<template>
  <div class="m-5">
    <table>
        <tr>
            <th>Name</th>
            <th>Place</th>
            <th>Location</th>
            <th>Capacity</th>
            <th>Action</th>
        </tr>
        <tr v-for="venue in venuelist" :key="venue.id">
            <td><a :href="`/admin/venuelink/${venue.id}`">{{ venue.name }}</a></td>
            <td>{{ venue.place }}</td>
            <td>{{ venue.location }}</td>
            <td>{{ venue.capacity }}</td>
            <td><a href="#" @click="venueupdate(venue)">Update</a></td>
            <VenueModification :id="venue.id" v-if="venue.Modifier" @close="venueupdated(venue)" @submit="submit"/>
        </tr>
        
    </table>
  </div>
    <footer><a class="m-5" href="/admin/dashboard">Back to home</a></footer>
</template>
<script>
import '../style.css'
import VenueModification from './VenueModification.vue';
import { url } from '@/functions/url';
//import alertify from 'alertifyjs';

export default{
    name:'ModifyVenue',
    components:{VenueModification},
    data(){
        return{
            username:'',
            email:'',
            venuelist:null,
            id:null,
        }
    },
    methods:{
        async get(url){
            const response = await fetch(url,{headers: {"cache":"off",
            Authorization: `Bearer ${localStorage.getItem('authToken')}`}});
        try{
            if(response.ok){
                const data = await response.json()
                this.venuelist = data
                console.log(data)
                console.log(this.venuelist)
                //alertify.alert(data.message)
        }
            else{
                console.log(response.statusText)
                //alertify.alert(response.statusText)
                }}
        catch(error){
            console.log(error);
            //alertify.alert(error)
    }},

    venueupdate(venue){
        venue.Modifier = true;
        this.id = venue.id;
    },

    venueupdated(venue){
        venue.Modifier = false;
        this.id = null;
    },
    async submit(data){
        try{
        const response = await fetch(`${url}api/venue`,{
            method:'PATCH',
            headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('authToken')}`
          },
            body:JSON.stringify({id:data.id,name:data.name,place:data.place,location:data.location,capacity:data.capacity})
        });
        if (response.ok) {
            for(let i=0;i<=this.venuelist.length;i++){
              if(this.venuelist[i].id == this.id){
                this.venuelist[i].Modifier = false;
                this.id = null;
              }
          }
          const json = await response.json();
          console.log(json.msg);
          
          //location.reload();
          
          
        }
        else {
            console.log(response.statusText);
          }}
          catch(error){
              console.log(error);
          }}

    },
    watch:{
        id(newValue,oldValue){
            console.log(`${oldValue} changed to ${newValue}`);
            if(newValue === null){
                location.reload();
            }
        }
    },
    mounted(){
        fetch(`${url}protected`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('authToken')}`
          }
        })
        .then(response => {
          // Check if the response status is 200 (OK)
          if (response.ok) {
            return response.json();
          } else {
            //throw new Error('Unauthorized');
            localStorage.removeItem('authToken');
            this.$router.push('/signin');
            //alert('Logged out successfully \n Redirecting to sign in page.')
          }
        })
        .then(data => {
          // Update the email value with the email received from the server
          this.username = data.username;
          this.email = data.email;
          this.get(`${url}api/venue`)
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
    }
}
</script>
<style scoped>
.modal{
display: flex;

}
th,
td {
  padding: 8px;
  text-align: center;
  border-bottom: 1px solid #ddd;
  border: 1px solid black;
}
th{
    background-color: #ccc;
}
</style>