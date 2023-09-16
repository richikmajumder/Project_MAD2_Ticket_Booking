<template>
  <div class="m-5">
    <table>
        <tr>
            <th>Name</th>
            <th>Rating</th>
            <th>Tags</th>
            <th>Actions</th>
        </tr>
        <tr v-for="show in showlist" :key="show.id">
            <td><a :href="`/admin/showlink/${show.id}`">{{ show.name }}</a></td>
            <td>{{ show.rating }}</td>
            <td>{{ show.tags }}</td>
            <td><a href="#" @click="showupdate(show)">Update</a></td>
            <ShowModification :id="show.id" v-if="show.Modifier" @close="showupdated(show)" @submit="submit"/>
        </tr>
        
    </table>
  </div>
    <footer><a class="m-5" href="/admin/dashboard">Back to home</a></footer>
</template>
<script>
import '../style.css'
import ShowModification from './ShowModification.vue';
import { url } from '@/functions/url';
//import alertify from 'alertifyjs';

export default{
    name:'ModifyShow',
    components:{ShowModification},
    data(){
        return{
            username:'',
            email:'',
            showlist:null,
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
                this.showlist = data
                console.log(data)
                console.log(this.showlist)
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

    showupdate(show){
        show.Modifier = true;
        this.id = show.id;
    },

    showupdated(show){
        show.Modifier = false;
        this.id = null;
    },
    async submit(data){
        try{
        const response = await fetch(`${url}api/show`,{
            method:'PATCH',
            headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('authToken')}`
          },
            body:JSON.stringify({id:data.id,name:data.name,rating:data.rating,tags:data.tags})
        });
        if (response.ok) {
            for(let i=0;i<=this.showlist.length;i++){
              if(this.showlist[i].id === this.id){
                this.showlist[i].Modifier = false;
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
          this.get(`${url}api/show`)
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