<template>
    <div class="modal">
   <center>
                <div class="modal-content">
                <span class="close" @click="closeForm">&times;</span>
                <h2>Remove Venue</h2>
                <!-- Add your form fields and submit button here -->
                <!--form @submit.prevent="submitForm"-->
                <!-- Form fields go here -->
                <table>
                    <tr>
                        <th>Venue Name</th>
                        <th>Venue Place</th>
                        <th>Venue Location</th>
                        <th>Venue Capacity</th>
                        <th>Action</th>
                    </tr>
                    <tr v-for="venue in list" :key="venue.id">
                        <td>{{ venue.name }}</td>
                        <td>{{ venue.place }}</td>
                        <td>{{ venue.location }}</td>
                        <td>{{ venue.capacity }}</td>
                        <td><span class="delete-icon" @click="Remove(venue)" title="Remove venue"><i class="bi bi-trash trash"></i></span></td>
                    </tr>
                </table>
                <!--/form-->
              </div>
    </center>
</div> 
</template>
<script>
import '../style.css';
import alertify from 'alertifyjs';
export default {
    name: 'RemoveVenue',
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
        capacity: null,
        id: null
      };
    },
    methods: {
      closeForm() {
        // Close the modal form
        this.$emit('close');
      },
      Remove(data){
          alertify.confirm('WARNING!!! This action is irreversible.','Do you really want to delete this venue?', ()=>{this.id = data.id;this.$emit('Remove',data)}, ()=>{this.id = null})
          //this.id = data;
          //this.$emit('Remove',data)

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

.delete-icon {
  cursor: pointer;
}

.trash {
  color: red;
}


</style>
  