<template>
    <div class="modal">
   <center>
                <div class="modal-content">
                <span class="close" @click="closeForm">&times;</span>
                <h2>Show Details</h2>
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
                    </tr>
                    <tr v-for="link in links" :key="link.id">
                        <td>{{ link.venue_name }}</td>
                        <td>{{ link.venue_place }}</td>
                        <td>{{ link.venue_location }}</td>
                        <td>{{ link.capacity }}</td>
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
    name:'ShowDetails',

    data(){
        return{
            show_id:null,
            name:'',
            tags:'',
            links:null,
            rating:null,
        }
    },
    methods:{
    closeForm(){
        this.$router.back()       
    }

    },
    mounted(){
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