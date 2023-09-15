<template>
<div v-if="status">
    <h4 class="heading">Update Password</h4>
  <div class="password-update-form">
    
    <form @submit.prevent="updatepassword">
      <label for="username">Username</label>
      <input type="text" name="username" placeholder="Enter your registered username" v-model="username" required :disabled="successfull">
      <br><br> 
      <label for="password">Password</label>
      <input type="password" name="password" placeholder="Set new password" v-model="password" minlength="8" required :disabled="successfull">
      <br><br>
      <label for="re-enter-password">Re-enter Password</label>
      <input type="password" name="re-enter-password" placeholder="Re-enter new password" v-model="check" minlength="8" required :disabled="successfull">
      <br><br>
      <button type="submit" v-if="password === check" class="btn btn-primary btn-sm" :disabled="successfull">Update Password</button>
      <p v-else-if="password != check" class="error-message">Passwords do not match.</p>
      <p v-if="successfull" class="text-success">Password updated successfully</p>
    </form>
  </div>
</div>
</template>

<script>
import { url } from '@/functions/url';
import alertify from 'alertifyjs';
import { hashify } from '@/functions/hash';

export default{
    name:'ResetPassword',
    data(){
        return{
            token:null,
            status:false,
            password:'',
            check:'',
            username:'',
            successfull:false

        }
    },
    methods:{
        async mount(){
        const response = await fetch(`${url}/api/reset/password/${this.token}`)        
            if(response.ok){
                const data = await response.json();
                if(data.message!='Token valid'){
                    alertify.alert('Reset link is invalid/expired')
                    setTimeout(()=>{this.$router.push('/signin')},2500)

                }
                else{
                    this.status=true
                    console.log(data.message)
                }
        }
            else{
                console.log(response.statusText)
                setTimeout(()=>{this.$router.push('/signin')},2500)
            }

        },
        async updatepassword(){
            const response = await fetch(`${url}api/reset/password`,{
            method:'POST',
            headers:{'Content-Type': 'application/json'},
            body:JSON.stringify({token:this.token,password:hashify(this.password),username:this.username})
             });
            if(response.ok){
              const data = await response.json();
              if(data.message=='Password updated successfully'){
                this.successfull=true;
                this.password='';
                this.check='';
                alert('Password changed successfully \n Please close this tab or it will automatically get closed within 5 seconds')
                setTimeout(()=>window.close(),5000)
              }
              else{
                alertify.alert(data.message);
                this.username='';
                this.password='';
                this.check='';
              }
            }
            else{
              alertify.alert(response.statusText)
            }
        }



    },
    mounted(){
        this.token = this.$route.params.token;
        this.mount()
        
    }
}
</script>
<style scoped>
/* Add your custom CSS styles here */
.password-update-form {
  text-align: center;
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

form {
  display:flex;
  flex-direction: column;
  align-items: center;
}

label {
  font-weight: bold;
  width: 200px;
}

input {
  padding: 8px;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 14px;
}

button {
  margin-top: 10px;
  padding: 8px 16px;
  font-size: 14px;
}

.error-message {
  color: #f00;
  font-size: 14px;
  font-weight: bold;
}

.heading{
    text-align: center;
}
</style>



