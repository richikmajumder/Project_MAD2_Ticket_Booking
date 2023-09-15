<template>
    <div class="modal">
   <center>
                <div class="modal-content">
                <span class="close" @click="closeForm">&times;</span>
                <h2>Update Show</h2>
                <!-- Add your form fields and submit button here -->
                <form method="PATCH">
                <!-- Form fields go here -->
                <label for="show">Show Name: </label>
                  <input type="text" v-model="name" placeholder="Show name" name="show" required><br><br>
                  <label for="tags">Tags: </label>
                  <select name="tags" v-model="tags" class="select" required>
                    <option value="Action">Action</option>
                    <option value="Comedy">Comedy</option>
                    <option value="Drama">Drama</option>
                    <option value="Sci-Fi">Sci-Fi</option>
                    <option value="Fiction">Fiction</option>
                    <option value="Horror">Horror</option>
                    <option value="Romance">Romance</option>
                  </select><br><br>
                  <label for="rating">Rating:</label>  
                  <select name="rating" v-model.number="rating" class="select" required>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                    <option value="4">4</option>
                    <option value="5">5</option>
                  </select>
                    <br><br>
                <!--/form-->
                  <button type="submit" @click="submitForm" class="btn btn-primary btn lg">Submit</button>
                </form>
                
                
              </div>
    </center>
</div> 

</template>

<script>
import { url } from '@/functions/url';
import '../style.css';
export default{
    name:'ShowModification',
    props:{
        id:{
            type:Number,
            required:true,
    }},

    data(){
        return{
            show_id:null,
            name:'',
            tags:'',
            rating:null
        }
    },
    methods:{
        closeForm(){
            this.$emit('close')
        },
        submitForm(event){
            event.preventDefault();
            this.$emit('submit',{id:this.show_id,name:this.name,tags:this.tags,rating:this.rating})
        }

    },
    mounted(){
        this.show_id=this.id;
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
          this.rating = data.show.rating;
          this.tags = data.show.tags;
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