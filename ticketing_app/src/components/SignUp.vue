<template>
  <div class="bg">
  <div><center><h1>Sign up</h1></center></div>
  
    <section class="vh-100">
      <form @submit.prevent="sendData">
  <div class="container py-5 h-100">
    <div class="row d-flex align-items-center justify-content-center h-100">
      <div class="col-md-8 col-lg-7 col-xl-6">
        <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-login-form/draw2.svg"
          class="img-fluid" alt="Phone image">
      </div>
     
      <div class="col-md-7 col-lg-5 col-xl-5 offset-xl-1">
          <!-- Email input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="form1Example13" >Email address</label>
            <input type="email" id="form1Example13" class="form-control form-control-lg" placeholder="Enter your email id" v-model="email" @input="emailTaken()" required/>
            <div v-if="emailtaken===null"></div>
            <div v-else-if="emailtaken" class="text-danger">
        <p>This email id is already registered.</p>
      </div>
      <!--<div v-else-if="!emailtaken" class="text-success">
        <p>This email id is available.</p>
      </div>-->
          </div>
          <!--Username-->
          <div class="form-outline mb-4">
            <label class="form-label" for="form1Example23" >Username</label>
            <input type="username" id="form1Example23" class="form-control form-control-lg" placeholder="Set an username" v-model="username" @input="usernameTaken()
            " required/>
            <div v-if="usernametaken===null"></div>
            <div v-else-if="usernametaken" class="text-danger">
        <p>This username is already taken.</p>
      </div>
      <!--<div v-else-if="!usernametaken" class="text-success">
        <p>The username is available.</p>
      </div>-->
          </div>
          <!--First Name-->
          <div class="form-outline mb-4">
            <label class="form-label" for="form1Example33" >First name</label>
            <input type="firstname" id="form1Example33" class="form-control form-control-lg" placeholder="Enter your first &middle(if any) name" v-model="first_name" required/>
            
          </div>
          <!--Last Name-->
          <div class="form-outline mb-4">
            <label class="form-label" for="form1Example43">Last name</label>
            <input type="lastname" id="form1Example43" class="form-control form-control-lg" placeholder="Enter your last name" v-model="last_name" required/>
            
          </div>
          <!-- Password input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="form1Example53">Password</label>
            <input type="password" id="form1Example53" class="form-control form-control-lg" placeholder="Password" v-model="password" required/>
            
          </div>
          <!-- Password input -->
          <div class="form-outline mb-4">
            <label class="form-label" for="form1Example63">Re-enter your password</label>
            <input type="password" id="form1Example63" class="form-control form-control-lg" placeholder="Re-enter your password" v-model="check" required/>
          </div>
            
          <div class="form-check form-switch" v-if="!this.$route.meta.isadmin">
            PDF report 
            <input class="form-check-input" type="checkbox" :checked="switchState" v-on:click="toggleSwitch"/>
            <label class="form-check-label">{{ switchState ? 'ON' : 'OFF' }}</label>
          </div>

          <!-- Submit button -->
          <div class="signup text-center">            
          <button type="submit" class="btn btn-primary btn-lg btn-block" v-if="emailtaken || usernametaken || password!=check "  disabled >Sign up</button>
          <button type="submit" class="btn btn-primary btn-lg btn-block" v-if="emailtaken==false && usernametaken==false && password.length>=8 && password==check " >Sign up</button>
</div>
          
          
      </div>
      <strong>Already registered? <a href="/signin">Sign In</a></strong>
    </div>
  </div>
</form>
</section>
<br><br><br><br><br><br><br><br>
<div class="text-center" >
<a href="/">Home</a>
</div>
</div>
</template>
<script>
import { hashify } from '../functions/hash.js'
import { url } from '@/functions/url';
export default{
    
    name: 'SignUp',
    data(){return {
        email:'',
        first_name:'',
        last_name:'',
        username:'',
        password:'',
        check:'',
        items:'',
        user:'',
        emailtaken: null,
        usernametaken: null,
        signupurl:'',
        switchState: false,
      }
      },
    methods: {
        async sendData() {
      const url = this.signupurl;
      const data = { email:this.email, firstname:this.first_name, lastname:this.last_name, username:this.username, password:await hashify(this.password), pdf_report:this.switchState };

      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        if (response.ok) {
          const json = await response.json();
          console.log(json);
          this.$router.push('/signin')
        } else {
            
          console.log(response.statusText);
        }
      } catch (error) {
        console.log(error);
      }
    },
    async emailTaken(){
        const response = await fetch(`${url}api/email/${this.email}`);
        if (response.ok){
          const data = await response.json();
          console.log(data);
          this.emailtaken = data;
        } else{
          console.log(response.statusText)
        } 
        
    },
    async usernameTaken(){
      const response = await fetch(`${url}api/username/${this.username}`);
      if (response.ok){
          const data = await response.json();
          console.log(data);
          this.usernametaken = data;
        } else{
          console.log(response.statusText)
        } 
    },
    toggleSwitch() {
        this.switchState = !this.switchState;
      }  
  },
  created(){
    const isAdminSignup = this.$route.meta.isadmin;
    this.signupurl = isAdminSignup ? `${url}api/admin/signup` : `${url}signup`;
  },
    mounted(){
        fetch(`${url}signup`).then(response => response.json())
      .then(data => {
        // Store the fetched data in the component's data property
        this.items = data;
        console.log(data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }
    }
    
</script>
<style scoped>
.bg{
  background-color: white;
}
</style>
