<template>
    <div class="modal">
   <center>
                <div class="modal-content">
                <span class="close" @click="closeForm">&times;</span>
                <h2>Remove Show</h2>
                <!-- Add your form fields and submit button here -->
                <!--form @submit.prevent="submitForm"-->
                <!-- Form fields go here -->
                <table>
                    <tr>
                        <th>Show Name</th>
                        <th>Show Rating</th>
                        <th>Show Tags</th>
                        <th>Action</th>
                    </tr>
                    <tr v-for="show in list" :key="show.id">
                        <td>{{ show.name }}</td>
                        <td>{{ show.rating }}</td>
                        <td>{{ show.tags }}</td>
                        <td><span class="delete-icon" @click="Remove(show)" title="Remove show"><i class="bi bi-trash trash"></i></span></td>
                    </tr>
                </table>
                <!--/form-->
              </div>
    </center>
</div> 
</template>
<script>
import '../style.css';
import alertify from 'alertifyjs';
export default {
    name: 'RemoveShow',
    props:{
        list:{
        type:Array,
        required:true,

    }
},
    data() {
      return {
        name: '',
        tags: '',
        rating: null,
        id: null
      };
    },
    methods: {
      closeForm() {
        // Close the modal form
        this.$emit('close');
      },
      Remove(data){
          alertify.confirm('WARNING!!! This action is irreversible.','Do you really want to delete this show?', ()=>{this.id = data.id;this.$emit('Remove',data)}, ()=>{this.id = null})
          //this.id = data;
          //this.$emit('Remove',data)

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

.delete-icon {
  cursor: pointer;
}

.trash {
  color: red;
}


</style>
  