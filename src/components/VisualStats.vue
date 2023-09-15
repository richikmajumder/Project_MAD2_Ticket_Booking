<template>
  <div>
    <h1 v-if="name==='venue'">Venue Stats</h1>
    <h1 v-else-if="name==='show'">Show Stats</h1>
    <h1 v-else-if="name==='popular'">Trending Show</h1>
    <p v-if="name==='venue'"><strong>Venue v/s Revenue</strong></p>
    <p v-else-if="name==='show'"><strong>Venue v/s Revenue</strong></p>
    <p v-else-if="name==='popular'"><strong>Popular Show</strong></p>
    <img :src="imageUrl" alt="Image" />
  </div>
</template>

<script>
//import { get } from '@/functions/get';
import { url } from '@/functions/url';
export default {
  name: 'VisualStats',
  props:{
    name:{
      type:String,
      required:true
    }
  },
  data() {
    return {
      imageUrl: '',
    };
  },
  methods: {
    async getImage() {
      try {
        const response = await fetch(`${url}api/stats?name=${this.name}`,{
            headers: {
            Authorization: `Bearer ${localStorage.getItem('authToken')}`
          }}); // Replace with the actual URL of your Flask API endpoint
        if (response.ok) {
          // If the response is successful, convert the image to a data URL and set it in the imageUrl variable
          const imageBlob = await response.blob();
          this.imageUrl = URL.createObjectURL(imageBlob);
        } else {
          this.$router.push('/signin');
          console.error('Failed to fetch image:', response.status, response.statusText);
        }
      } catch (error) {
        console.error('Error fetching image:', error);
  }
}
  },
  mounted(){
    this.getImage();

  },
  watch:{
    name(oldValue,newValue){
      console.log(oldValue)
      console.log(newValue)
      this.getImage();

    }
  }
}
    
</script>

