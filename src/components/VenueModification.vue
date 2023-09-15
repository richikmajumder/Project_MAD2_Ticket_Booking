<template>
    <div class="modal">
   <center>
                <div class="modal-content">
                <span class="close" @click="closeForm">&times;</span>
                <h2>Update Venue</h2>
                <!-- Add your form fields and submit button here -->
                <form method="PATCH">
                <!-- Form fields go here -->
                <label for="venue">Venue Name: </label>
                  <input type="text" v-model="name" placeholder="Show name" name="venue" required><br><br>
                  <label for="place">Place:</label>  
                  <input type="text" v-model="place" placeholder="Place" name="place" required><br><br>
                  <label for="location">Location:</label>  
                  <input type="text" v-model="location" placeholder="Location" name="location" required><br><br>
                  <label for="capacity">Capacity:</label>  
                  <input type="number" v-model="capacity" placeholder="Capacity" name="capacity" required><br><br>
                <!--/form-->
                  <button type="submit" @click="submitForm" class="btn btn-primary btn lg">Submit</button>
                </form>
                
                
              </div>
    </center>
</div> 

</template>

<script>
import '../style.css';
import { url } from '@/functions/url';
export default{
    name:'VenueModification',
    props:{
        id:{
            type:Number,
            required:true,
    }},

    data(){
        return{
            venue_id:null,
            name:'',
            place:'',
            location:'',
            capacity:null,
        }
    },
    methods:{
        closeForm(){
            this.$emit('close')
        },
        submitForm(event){
            event.preventDefault();
            this.$emit('submit',{id:this.venue_id,name:this.name,place:this.place,location:this.location,capacity:this.capacity})
        }

    },
    mounted(){
        this.venue_id=this.id;
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
          this.place = data.venue.place;
          this.location = data.venue.location;
          this.capacity = data.venue.capacity;
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
</style>