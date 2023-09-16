<template>
    <div class="modal">
   <center>
                <div class="modal-content">
                <span class="close" @click="closeForm">&times;</span>
                <h2>Venues</h2>
                <!-- Add your form fields and submit button here -->
                <!--form @submit.prevent="submitForm"-->
                <!-- Form fields go here -->
                <table>
                    <tr>
                        <th>Venue Name</th>
                        <th>Venue Place</th>
                        <th>Venue Location</th>
                        <th>Venue Capacity</th>
                    </tr>
                    <tr v-for="venue in list" :key="venue.id">
                        <td><a :href="`/venue/details/${venue.id}`">{{ venue.name }}</a></td>
                        <td>{{ venue.place }}</td>
                        <td>{{ venue.location }}</td>
                        <td>{{ venue.capacity }}</td>
                    </tr>
                </table>
              </div>
    </center>
</div> 
</template>
<script>
import '../style.css';
export default {
    name: 'VenueList',
    props:{
        list:{
        type:Array,
        required:true,

    }
},
    data() {
      return {
        name: '',
        place: '',
        location: '',
        capacity: null
      };
    },
    methods: {
      closeForm() {
        // Close the modal form
        this.$emit('close');
      },
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
  