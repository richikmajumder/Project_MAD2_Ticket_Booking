<template>
    <div class="modal">
   <center>
                <div class="modal-content">
                <span class="close" @click="closeForm">&times;</span>
                <h2>Show name: {{ name }}</h2>
                <!-- Add your form fields and submit button here -->
                <table>
                    <tr>
                        <th>Venue Name</th>
                        <th>Venue Place</th>
                        <th>Venue Location</th>
                        <th>Venue Capacity</th>
                        <th>Date</th>
                        <th>Start Time</th>
                        <th>Ticket Price</th>
                        <th>Actions</th>
                    </tr>
                    <tr v-for="link in links" :key="link.id">
                        <td>{{ link.venue_name }}</td>
                        <td>{{ link.venue_place }}</td>
                        <td>{{ link.venue_location }}</td>
                        <td>{{ link.capacity }}</td>
                        <td>{{ link.date }}</td>
                        <td>{{ link.time }}</td>
                        <td>{{ link.ticket_price }}</td>
                        <td>
                            <a href="#"  @click="openShowLinkModification(link)">Update</a> &nbsp;
                            <span class="delete-icon" @click="erase(link)" title="Delink show"><i class="bi bi-trash trash"></i></span>
                        <ShowLinkModification :id="link.id" v-if="link.Modifier" v-on:close="closeShowLinkModification(link)" v-on:submit="submit" />
                        </td>
                    </tr>
                </table>
              </div>
    </center>
   

</div> 

</template>

<script>
import '../style.css';
import { remove } from '../functions/remove.js';
import { url } from '@/functions/url';
import alertify from 'alertifyjs';
import ShowLinkModification from './ShowLinkModification.vue';

export default{
    name:'ShowLink',
    components:{ShowLinkModification},

    data(){
        return{
            id:null,
            show_id:null,
            name:'',
            tags:'',
            links:null,
            rating:null,
        }
    },
    methods:{
    closeForm(){
        if(localStorage.getItem('authToken')){
            this.$router.push('/modify/show')

        }
        else{
            this.$router.push('/')
        }
    },
    async reactiveDelete(payload){ await remove(`http://127.0.0.1:8080/api/admin/showlink/delink/${payload.id}`);location.reload();},
    erase(payload){
        alertify.confirm('WARNING!!! This action is irreversible.','Do you really want to delink this venue?', ()=>{this.reactiveDelete(payload)},()=>console.log(payload))
    },
    openShowLinkModification(data){
        data.Modifier = true;
        this.id = data.id;
    },
    closeShowLinkModification(data){
        data.Modifier = false;
        this.id = null;
    },
    async submit(data){
        try{
        const response = await fetch(`${url}api/admin/showlink`,{
            method:'PATCH',
            headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('authToken')}`
          },
            body:JSON.stringify(data)
        });
        if (response.ok) {
            for(let i=0;i<=this.links.length;i++){
              if(this.links[i].id === this.id){
                this.links[i].Modifier = false;
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
    mounted(){
        fetch(`${url}protected`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('authToken')}`
          }
        })
        .then(response => {
          // Check if the response status is 200 (OK)
          if (response.ok) {
            this.$store.commit('role','admin')
            this.show_id=this.$route.params.id;
        fetch(`${url}api/show?id=${this.show_id}`,{
            headers: {
            Authorization: `Bearer ${localStorage.getItem('authToken')}`
          },
        }).then(response => {
          // Check if the response status is 200 (OK)
          if (response.ok) {
            return response.json();
          }
          else{
              this.$router.push('/signin')
          }
        })
        .then(data => {
          // Update the email value with the email received from the server
          this.name = data.show.name;
          this.show_id = data.show.id;
          this.rating = data.show.rating;
          this.tags = data.show.tags;
          this.links = data.links;
        })
        .catch(error =>{
            console.log(error);
            
        })

            return response.json();
          } else {
            //throw new Error('Unauthorized');
            localStorage.removeItem('authToken');
            this.$store.commit('role',null);
            this.$router.push('/signin');
            //alert('Logged out successfully \n Redirecting to sign in page.')
          }
        })
        
    },
    watch:{
        id(newValue,oldValue){
            console.log(`${oldValue} changed to ${newValue}`)
            if(newValue===null){
            location.reload();
            }
        }

    }
}
</script>
<style scoped>
.modal{
display: flex;

}


th,
td {
    border:1px solid black;
}
.delete-icon {
  cursor: pointer;
}

.trash {
  color: red;
}
</style>