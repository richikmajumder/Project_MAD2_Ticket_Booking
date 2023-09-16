<template>
    <div class="modal">
   <center>
                <div class="modal-content">
                <span class="close" @click="closeForm">&times;</span>
                <h2>Update Profile</h2>
                <!-- Add your form fields and submit button here -->
                <form method="PATCH" @submit.prevent="updateProfile" >
                <!-- Form fields go here -->
                <label for="username">Username</label>
                <input type="text" name="username" placeholder="username" v-model="Username" disabled required/><br><br>
                <label for="email">Email</label>
                <input type="email" name="email" placeholder="Email" v-model="email" disabled required/><br><br>
                <label for="first_name">First name</label>
                <input type="text" name="first_name" placeholder="First Name" v-model="first_name" required/><br><br>
                <label for="last_name">Last name</label>
                <input type="text" name="last_name" placeholder="Last Name" v-model="last_name" required/><br><br>

                <center>
                    <div class="form-check form-switch" v-if="!admin">PDF monthly report 
                &nbsp; &nbsp;<input class="form-check-input" type="checkbox" :checked="switchState" v-on:click="toggleSwitch" id="report"/>
                <label for="report" class="form-check-label">{{ switchState ? 'ON' : 'OFF' }}</label>
                <br><br>
                </div>
                </center>
                
                <div>
                <label for="changepassword">Update Password</label>
                <input type="checkbox" v-model="changepassword" id="changepassword" value="true" />
                <br><br>
                </div>
                <div v-if="changepassword">
                <label for="password">Password</label>
                <input type="password" minlength="8" name="password" placeholder="Set new password" v-model="password" required/><br><br>
                <label for="password">Re-enter password</label>
                <input type="password" minlength="8" name="password" placeholder="Re-type new password" v-model="check" required/><br><br>
                </div>
                <button type="submit" class="btn btn-primary btn-sm" value="Update Profile" v-if="password===check" >Update Profile</button>
                </form>
                </div>
    </center>
    </div>

</template>

<script>
import { get } from '@/functions/get';
import { hashify } from '@/functions/hash';
import { url } from '@/functions/url';
import alertify from 'alertifyjs';
//import '../style.css';
export default{
    name:'UpdateProfile',
    props:{
        username:{
            type:String,
            required:true
        },
    },
    data(){
            return{
                Username:'',
                email:'',
                first_name:'',
                last_name:'',
                admin:null,
                password:'',
                check:'',
                changepassword:false,
                switchState:false

            }
    },
    methods:{
        async updateProfile(){
        if(this.admin){
            if(this.changepassword){
                var payload = {username:this.Username,first_name:this.first_name,last_name:this.last_name,password:hashify(this.password)}
            }
            else{
                 payload = {username:this.Username,first_name:this.first_name,last_name:this.last_name}
            }}
        else if(!this.admin){
            if(this.changepassword){
                 payload = {username:this.Username,first_name:this.first_name,last_name:this.last_name,password:hashify(this.password),pdf_report:this.switchState}
            }
            else{
                 payload = {username:this.Username,first_name:this.first_name,last_name:this.last_name,pdf_report:this.switchState}
            }}

        
        const response = await fetch(`${url}api/profile`,{headers:{'Content-type':'application/json',
            Authorization: `Bearer ${localStorage.getItem('authToken')}`},method:'PATCH',body:JSON.stringify(payload)});
            if(response.ok){
                const data = await response.json()
                 alertify.alert(data.message)
        }
            else{
                alertify.alert('Something went wrong')
        }
            this.$emit('close')
        },
        closeForm(){
            this.$emit('close')
        },
        toggleSwitch() {
        this.switchState = !this.switchState;
      }  


    },
    mounted(){
        this.Username = this.username
        get(`${url}api/profile?username=${this.username}`).then(data=>{
            this.email=data.email;
            this.first_name=data.first_name;
            this.last_name=data.last_name;
            this.admin=data.admin;
            if(!this.admin){
                this.switchState=data.pdf_report;
            }
        })
    }
    }


</script>
<style scoped>

</style>