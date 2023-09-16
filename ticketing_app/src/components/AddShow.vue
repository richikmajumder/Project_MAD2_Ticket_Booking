<template>
    <div class="modal">
   <center>
                <div class="modal-content">
                <span class="close" @click="closeForm">&times;</span>
                <h2>Add new show</h2>
                <!-- Add your form fields and submit button here -->
                <form @submit.prevent="submitForm">
                <!-- Form fields go here -->
                <label for="show">Show Name: </label>
                  <input type="text" v-model="name" placeholder="Show name" name="show" @input="showAvailability()" required><br><br>
                <div v-if="!hide">
                <label for="rating" class="label">Rating:</label>  
                  <select name="rating" v-model.number="rating" class="select" required>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                  </select>
                    <br><br>
                  <label for="tags">Tags: </label>
                  <select name="tags" v-model="tags" class="select" required>
                    <option value="Action">Action</option>
                    <option value="Comedy">Comedy</option>
                    <option value="Drama">Drama</option>
                    <option value="Sci-Fi">Sci-Fi</option>
                    <option value="Fiction">Fiction</option>
                    <option value="Horror">Horror</option>
                    <option value="Romance">Romance</option>
                  </select>
                  <br><br>
                  </div>
                  <label for="venue" class="label">Venue</label>  
                  <select name="venue" v-model="venue" class="select">
                    <option v-for="Venue in list" :key="Venue.id" :value="Venue" required>{{ Venue.name }} {{ Venue.place }} {{ Venue.location }}</option>
                  </select><br><br>
                  <label for="date">Date: </label>
                  <input type="date" v-model="date" placeholder="Show date" name="date" required><br><br>
                  <label for="time">Time: </label>
                  <input type="time" v-model="time" placeholder="Show start time" name="time" required><br><br>
                  <label for="price">Ticket price: ₹</label>
                  <input type="number" v-model="price" :min=0 placeholder="Ticket price in ₹" name="price" required><br><br>
                  <button type="submit" v-if="venue" class="btn btn-primary btn-lg">Submit</button>
                  
                </form>
              </div>
    </center>
</div> 
</template>
<script>
import { url } from '@/functions/url';
//import '../style.css';
export default {
    name: 'AddShow',
    props: {
      list:{
        type:Array,
        required:true
      }
    },
    data() {
      return {
        name: '',
        rating: null,
        tags: '',
        venue: null,
        date: null,
        time: null,
        price: null,
        hide: false
      };
    },
    methods: {
      submitForm() {
        // Handle form submission logic
        // You can emit an event or call a method in the parent component to handle the form data
        this.$emit('submitData',{name:this.name,rating:this.rating,tags:this.tags,venue_id:this.venue.id,venue_name:this.venue.name,venue_place:this.venue.place,venue_location:this.venue.location,date:this.date,time:this.time,price:this.price})
      },
      closeForm() {
        // Close the modal form
        this.$emit('close');
      },
      async showAvailability() {
        if(this.name!=''){
        const response = await fetch(`${url}api/show/${this.name}`,{headers: {
        Authorization: `Bearer ${localStorage.getItem('authToken')}`
      }});
      if(response.ok){
        const data = await response.json();
        if(data.message){
          this.hide=true;
          this.name=data.name;
        }
        else{
          this.hide=false;
          console.log(data.message)
        }
      }
      else{
        console.log(response.statusText)
      }
      }
    }
    },
  };
</script>
  