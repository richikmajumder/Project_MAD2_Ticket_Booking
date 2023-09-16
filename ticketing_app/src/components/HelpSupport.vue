<template>
    <div class="modal">
     <center>
    <div class="modal-content">
    <span class="close" @click="closeForm">&times;</span>
    <p></p><p></p>
    <h4>For any kind of help or support, feel free to drop an email</h4>
    <p>Email:-<strong>21f1000460@ds.study.iitm.ac.in</strong></p>
    </div>
    </center>
    </div>
</template>
<script>
export default{
    name:'HelpSupport',
    methods:{
        closeForm(){
            this.$emit('close');
        }
    }
}
</script>