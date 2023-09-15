<template>
    <div class="modal">
   <center>
                <div class="modal-content">
                <span class="close" @click="closeForm">&times;</span>
                <h2>Shows</h2>
                <!-- Add your form fields and submit button here -->
                <!--form @submit.prevent="submitForm"-->
                <!-- Form fields go here -->
                <table>
                    <tr>
                        <th>Show Name</th>
                        <th>Rating</th>
                        <th>Tags</th>
                    </tr>
                    <tr v-for="show in list" :key="show.id">
                        <td><a :href="`/show/details/${show.id}`">{{ show.name }}</a></td>
                        <td>{{ show.rating }}</td>
                        <td>{{ show.tags }}</td>
                    </tr>
                </table>

              </div>
    </center>
</div> 
</template>
<script>
//import '../style.css';
export default {
    name: 'ShowList',
    props:{
        list:{
        type:Array,
        required:true,

    }
},
    data() {
      return {
        name: '',
        rating: '',
        tags: '',
        id:null,
      };
    },
    methods: {
      closeForm() {
        // Close the modal form
        this.$emit('close');
      },
      showfetch(show){
          show.Modifier = true;
          this.id = show.id;
      },
      closeshowfetch(show){
          show.Modifier = false;
      }
    },
    watch:{
      list(newValue,oldValue){
        if(newValue){
          console.log(newValue==oldValue)
        }
      }
    },
  };
</script>
<style scoped>

th,
td {
  padding: 8px;
  text-align: center;
  border-bottom: 1px solid #ddd;
  border: 1px solid black;
}




</style>
  