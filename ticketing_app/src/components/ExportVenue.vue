<template>
    <div class="modal">
   <center>
                <div class="modal-content">
                <span class="close" @click="closeForm">&times;</span>
                <h2>Export venue</h2>
                <!-- Add your form fields and submit button here -->
                <!--form @submit.prevent="submitForm"-->
                <!-- Form fields go here -->
                <table>
                    <tr>
                        <th>Venue Name</th>
                        <th>Venue Place</th>
                        <th>Venue Location</th>
                        <th>Actions</th>
                    </tr>
                    <tr v-for="venue in list" :key="venue.id">
                        <td>{{ venue.name }}</td>
                        <td>{{ venue.place }}</td>
                        <td>{{ venue.location }}</td>
                        <td><button class="btn btn-primary btn-sm" @click="exporttask('http://127.0.0.1:8080/api/venue/export',{username:username,venue_id:venue.id})">Export</button></td>
                    </tr>
                </table>
                <!--/form-->
              </div>
    </center>
</div> 
</template>
<script>
import '../style.css';
import { update } from '@/functions/update';
import { url } from '@/functions/url';
export default {
    name: 'ExportVenue',
    props:{
        list:{
        type:Array,
        required:true,
    },
    username:{
        type:String,
        required:true,
    }
},
    data() {
      return {
        
      };
    },
    methods: {
      closeForm() {
        // Close the modal form
        console.log(url)
        this.$emit('close');
      },
      exporttask(url,payload){
          update(url,payload,this.$router)

      }
    },
  };
</script>
<style scoped>

th,
td {
  padding: 8px;
  text-align: center;
  border-bottom: 1px solid #ddd;
  border: 1px solid black;
}




</style>
  