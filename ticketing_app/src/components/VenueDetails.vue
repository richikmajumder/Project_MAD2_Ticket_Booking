<template>
    <div class="modal">
   <center>
                <div class="modal-content">
                <span class="close" @click="closeForm">&times;</span>
                <h2>Venue Details</h2>
                <!-- Add your form fields and submit button here -->
                <table>
                    <tr>
                        <th>Show Name</th>
                        <th>Rating</th>
                        <th>Tags</th>
                        <th>Date</th>
                        <th>Start Time</th>
                        <th>Ticket Price</th>
                    </tr>
                    <tr v-for="link in links" :key="link.id">
                        <td>{{ link.show_name }}</td>
                        <td>{{ link.rating }}</td>
                        <td>{{ link.tags }}</td>
                        <td>{{ link.date }}</td>
                        <td>{{ link.time }}</td>
                        <td>{{ link.ticket_price }}</td>
                    </tr>
                </table>
              </div>
    </center>
   

</div> 

</template>

<script>
import '../style.css';
import { url } from '@/functions/url';
export default{
    name:'VenueDetails',

    data(){
        return{
            venue_id:null,
            name:'',
            place:'',
            location:'',
            links:null,
            capacity:null,
        }
    },
    methods:{

    closeForm(){
        this.$router.back()   
    }

    },
    mounted(){
        this.venue_id=this.$route.params.id;
        fetch(`${url}api/venue?id=${this.venue_id}`,{
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
          this.name = data.venue.name;
          this.venue_id = data.venue.id;
          this.place = data.venue.place;
          this.location = data.venue.location;
          this.capacity = data.venue.capacity;
          this.links = data.links;
        })
        .catch(error =>{
            console.log(error);
            
        })
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

</style>