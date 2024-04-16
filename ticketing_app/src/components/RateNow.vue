<template>
    <div class="modal">
     <center>
    <div class="modal-content">
    <span class="close" @click="closeForm">&times;</span>
    <h1>Please rate the show:</h1>
    <form @submit.prevent="rate(`http://127.0.0.1:8080/api/bookinghistory`,{show_id:show_id,user_id:user_id,rating:rating})" method="POST">
        <div class="rating">
            <input type="radio" name="rating" id="rating-5" value=5 v-model="rating">
            <label for="rating-5">&#9733;</label>
            <input type="radio" name="rating" id="rating-4" value=4 v-model="rating">
            <label for="rating-4">&#9733;</label>
            <input type="radio" name="rating" id="rating-3" value=3 v-model="rating">
            <label for="rating-3">&#9733;</label>
            <input type="radio" name="rating" id="rating-2" value=2 v-model="rating">
            <label for="rating-2">&#9733;</label>
            <input type="radio" name="rating" id="rating-1" value=1 v-model="rating">
            <label for="rating-1">&#9733;</label>
        </div>
        <button type="submit" v-if="rating">Submit Rating</button>
    </form>
    </div>
    </center>
    </div>
</template>
<script>
import '../style.css'
import { update } from '@/functions/update';
import { url } from '@/functions/url';
export default{
    name:'RateNow',
    props:{
        show_id:{
            type:Number,
            required:true
        },
        user_id:{
            type:Number,
            required:true
        }
    },
    data(){
        return{
            rating:null,
        }
    },
    methods:{
        closeForm(){
            console.log(url)
            this.$emit('close');
        },
        async rate(url,payload){
            //console.log(url)
            //console.log(payload)
            await update(url,payload,this.$router)
            this.$emit('close');
        }
    }
}
</script>
<style scoped>
.rating {
            display: flex;
            flex-direction: row-reverse;
            justify-content: center;
            align-items: center;
            height: 40px;
            margin-bottom: 20px;
        }
        
        .rating input {
            display: none;
        }
        
        .rating label {
            font-size: 30px;
            color: #ccc;
            cursor: pointer;
            transition: all 0.5s;
        }
        
        .rating label:hover,
        .rating label:hover ~ label,
        .rating input:checked ~ label {
            color: #ffc107;
        }
        .modal{
display: flex;

}
</style>
