<template>
    <center>
    <div class="card text-center" style="width: 300px;">
    <div class="card-header h5 text-white bg-primary">Password Reset</div>
    <div class="card-body px-5">
        <p class="card-text py-2">
            Enter your email address and we'll send you an email with instructions to reset your password.
        </p>
        <form @submit.prevent="sendlink">
        <div class="form-outline">
            <input type="email" id="typeEmail" class="form-control my-3" v-model="email" placeholder="Enter your registered email address"/>
        </div>
        <button href="#" class="btn btn-primary w-100" v-if="email!=null" >Reset password</button>
    </form>
        <div class="d-flex justify-content-between mt-4">
            <a class="" href="/signin">Sign in</a>
            <a class="" href="/">Home</a>
        </div>
    </div>
</div>
</center>
    </template>
    
    <script>
    import { url } from '@/functions/url';
    import { update } from '@/functions/update';
    export default{
        name:'ForgotPassword',
        data(){
            return{
                email:null
            }

        },
        methods:{
            async sendlink(){
                await update(url+'api/forgot/password',{email:this.email},this.$router)
                
                
            }

        }
    }
    </script>
