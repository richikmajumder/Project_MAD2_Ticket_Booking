<template>
    <div class="modal">
   <center>
                <div class="modal-content">
                <span class="close" @click="closeForm">&times;</span>
                <h2>Add new venue</h2>
                <!-- Add your form fields and submit button here -->
                <form @submit.prevent="submitForm">
                <!-- Form fields go here -->
                <label for="venue">Venue Name: </label>
                  <input type="text" v-model="name" placeholder="Venue name" name="venue" required><br><br>
                  <label for="place">Place:</label>  
                  <input type="text" v-model="place" placeholder="Place" name="place" required><br><br>
                  <label for="location">Location:</label>  
                  <input type="text" v-model="location" placeholder="Location" name="location" required><br><br>
                  <label for="capacity">Capacity:</label>  
                  <input type="number" v-model="capacity" placeholder="Capacity" name="capacity" required><br><br>
                  <button type="submit" class="btn btn-primary btn-lg" >Submit</button>
                </form>
              </div>
    </center>
</div> 
</template>
<script>
//import '../style.css';
export default {
    name: 'AddVenue',
    data() {
      return {
        name: '',
        place: '',
        location: '',
        capacity: null
      };
    },
    methods: {
      submitForm() {
        // Handle form submission logic
        // You can emit an event or call a method in the parent component to handle the form data
        this.$emit('submitData',{name:this.name,place:this.place,location:this.location,capacity:this.capacity})
      },
      closeForm() {
        // Close the modal form
        this.$emit('close');
      },
    },
  };
</script>
  