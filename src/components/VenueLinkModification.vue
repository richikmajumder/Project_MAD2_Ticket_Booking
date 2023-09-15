<template>
    <div class="modal">
   <center>
                <div class="modal-content">
                <span class="close" @click="closeForm">&times;</span>
                <h2>Update Show link</h2>
                <!-- Add your form fields and submit button here -->
                <form method="PATCH">
                <!-- Form fields go here -->
                <label for="show">Show Name: </label>
                  <input type="text" v-model="name" placeholder="Show name" name="show" required disabled><br><br>
                  <label for="tags">Tags:</label>  
                  <input type="text" v-model="tags" placeholder="Tags seperated by ','" name="tags" required disabled><br><br>
                  <label for="rating">Rating:</label>  
                  <select name="rating" v-model.number="rating" class="select" required disabled>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                  </select>
                    <br><br>
                    <label for="date">Date</label>
                  <input type="date" v-model="date" placeholder="Date" name="date" required><br><br>
                  <label for="time">Time</label>
                  <input type="time" v-model="time" placeholder="Show start time" name="time" required><br><br>
                  <label for="price">Ticket price</label>
                  <input type="number" v-model="price" placeholder="₹" name="price" required><br><br>
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
    name:'ShowModification',
    props:{
        id:{
            type:Number,
            required:true,
    }},

    data(){
        return{
            link_id:null,
            venue_id:null,
            show_id:null,
            name:'',
            tags:'',
            rating:null,
            date:'',
            time:'',
            price:null,
        }
    },
    methods:{
        closeForm(){
            this.$emit('close')
        },
        submitForm(event){
            event.preventDefault();
            this.$emit('submit',{id:this.link_id,venue_id:this.venue_id,show_id:this.show_id,name:this.name,tags:this.tags,rating:this.rating,date:this.date,time:this.time,price:this.price})
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
            this.$store.commit('role','admin');
            this.link_id=this.id;
        fetch(`${url}api/admin/venuelink?id=${this.link_id}`,{
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
          this.name = data.show_name;
          this.rating = data.rating;
          this.tags = data.tags;
          this.show_id = data.show_id;
          this.venue_id = data.venue_id;
          this.time = data.time;
          this.date = data.date;
          this.price = data.ticket_price;
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
        this.link_id=this.id;
        fetch(`${url}api/admin/venuelink?id=${this.link_id}`,{
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
          this.name = data.show_name;
          this.rating = data.rating;
          this.tags = data.tags;
          this.show_id = data.show_id;
          this.venue_id = data.venue_id;
          this.time = data.time;
          this.date = data.date;
          this.price = data.ticket_price;
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