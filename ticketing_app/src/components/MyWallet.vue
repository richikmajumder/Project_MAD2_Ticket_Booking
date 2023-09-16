<template>
    <div v-if="balance === null">
      <button class="btn btn-primary btn-sm" @click="activate">Activate wallet</button>
    </div>
    <div v-else-if="balance >= 0">
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
      Your wallet balance is ₹{{ balance }}<br>
      <p></p>
      <form @submit.prevent="addMoney" class="add-money-form">
        <label for="addmoney">Add money:</label> ₹
        <input type="number" name="addmoney" v-model="load" min="10" max="10000" placeholder="min ₹10 and max of ₹10000" >
        <button class="btn btn-primary btn-sm" type="submit" v-if="load >= 10">Add Money</button>
      </form>
    </div>
</template>

<script>
import { get } from '@/functions/get';
import { url } from '../functions/url';
import alertify from 'alertifyjs';
export default{
    name:'MyWallet',
    props:{
        username:{
            type:String,
            required:true
        }
    },
    data(){
        return{
            balance:null,
            load:null

        }
    },
    methods:{
        async activate(){
            const response = await fetch(`${url}/api/wallet`,{
                method:'PATCH',
                headers:{'Content-Type': 'application/json',
                Authorization: `Bearer ${localStorage.getItem('authToken')}`,},
                body:JSON.stringify({add_money:0,username:this.username})});

                if(response.ok){
                    const data = await response.json()
                    alertify.alert(data.message)
                    location.reload();
                }
                else{
                    alertify.alert((await response).statusText)
                    
                }
        },
        async addMoney(){
            const response = await fetch(`${url}/api/wallet`,{
                method:'PATCH',
                headers:{'Content-Type': 'application/json',
                Authorization: `Bearer ${localStorage.getItem('authToken')}`,},
                body:JSON.stringify({add_money:this.load,username:this.username})});

                if(response.ok){
                    const data = await response.json()
                    await alertify.alert(data.message)
                    setTimeout(()=>{location.reload()},5000)
                }
                else{
                    alertify.alert((await response).statusText)
                    
                }
            
            
        }

    },
    mounted(){
        console.log(url)
        get(`${url}/api/wallet?username=${this.username}`).then(data=>this.balance=data)
        
    }
}

</script>
<style>
.add-money-form {
  margin-top: 10px;
}
.add-money-form input {
  margin-right: 10px; /* Add space on the right side of the input */
}
</style>