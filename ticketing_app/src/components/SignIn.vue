<template>
  <div class="bg">
  <div>
    <center>
      <h1>Sign in</h1>
    </center>
  </div>
  <section class="vh-100">
    <div class="container py-5 h-100">
      <div class="row d-flex align-items-center justify-content-center h-100">
        <div class="col-md-8 col-lg-7 col-xl-6">
          <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.svg" class="img-fluid" alt="Phone image">
        </div>
        <div class="col-md-7 col-lg-5 col-xl-5 offset-xl-1">
          <!-- Email input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="form1Example13">Email/username</label>
            <input type="username" id="form1Example13" class="form-control form-control-lg" placeholder="username/email" v-model="username">
          </div>

          <!-- Password input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="form1Example23">Password</label>
            <input type="password" id="form1Example23" class="form-control form-control-lg" placeholder="password" v-model="password">
          </div>


          <div class="d-flex justify-content-around align-items-center mb-4">
            <!-- Checkbox -->
            <a href="/forgot/password">Forgot password?</a>
             

          </div>

          <div class="text-center">
            <!-- Submit button -->
            <button type="submit" class="btn btn-primary btn-lg btn-block" v-on:click="sendData">Sign in</button>
            
          </div>
          
        </div>
        <strong>New user? <a href="/signup">Sign Up</a></strong>
             
      </div>
    </div>
  </section>
  <div class="text-center">
    <a href="/">Home</a>
  </div>
</div>
  
</template>


<script>
import { hashify } from '../functions/hash.js'
import { url } from '@/functions/url';
import alertify from 'alertifyjs';
export default {
    name : 'SignIn',
    data(){
      return{
        email:'',
        username:'',
        password:''
      }

    },
    methods: {
        async sendData(){
            const response = await fetch(`${url}signin`,{
                method:'POST',
                headers:{'Content-Type': 'application/json'},
                body:JSON.stringify({username:this.username,password:hashify(this.password)})
            });
            if (response.ok) {
          const json = await response.json();
          console.log(json.access_token);
          //const token = JSON.stringify(json)
          localStorage.setItem('authToken',json.access_token);
          //console.log(localStorage.getItem('authToken'))
          if (json.role=='user'){this.$router.push('/protected')}
          else if(json.role=='admin'){
            this.$router.push('/admin/dashboard')
          }
          else{
            this.$router.push('/signin')
          }
          
        } else {
          const data = await response.json()
          alertify.alert(data.message)  
          //console.log(response.statusText);
        }
      
        }
    }

}
</script>
<style scoped>
.bg{
  background-color: white;
}
</style>