<template>
   
    <div v-if="element.type==='Venue name' || element.type==='Location'" class="m-5">
        
      <!-- Display the received element data -->
      <h1>Search Result Details</h1>
      <p v-if="element.type==='Location'">Location:{{ element.location }}</p>
      <p>Venue: {{ element.result }}</p>
      <!-- Add more details from the element as needed -->
      <label for="rating">Filter by rating:</label>
      <select v-model="selectedRating" name="rating">
      <option v-for="rating in availableRatings" :key="rating" :value="rating">{{ rating }}</option>
    </select>

    <!-- Filter options for tags (assuming tags is an array of available tags) -->
    <label for="tags">Filter by tags:</label>
    <select v-model="selectedTags" name="tags">
      <option v-for="tag in tags" :key="tag" :value="tag">{{ tag }}</option>
    </select>

    &nbsp;
    <button @click="removeFilter" v-if="selectedTags.length > 0 || selectedRating" class="btn btn-secondary btn-sm">Reset Filter</button>
    <!-- Display the filtered links -->
    <table>
      <tr>
          <th>Show Name</th>
          <th>Tags</th>
          <th>Rating</th>
          <th>Date</th>
          <th>Time</th>
          <th>Ticket Price</th>
          <th v-if="localstoragecheck('user')">Book Now</th>
        </tr>
    <tr v-for="link in filteredLinks" :key="link.id">
            <td>{{ link.show_name }}</td>
            <td>{{ link.tags }}</td>
            <td>{{ link.rating }}</td>
            <td>{{ link.date }}</td>
            <td>{{ link.time }}</td>
            <td>{{ link.ticket_price }}</td>
            <td v-if="localstoragecheck('user')"><button class="btn btn-primary btn-sm" v-if="link.tickets_left>0" @click="book(link.link_id)">Book Now</button>
              <button class="btn btn-grey btn-sm" v-else disabled>Sold out</button></td>
      </tr>
    <!-- ... (table header) -->
      
  </table>
    
      
    
    </div>
    <div v-if="element.type==='Show name'" class="m-5">
       <!-- Display the received element data -->
       <h1>Search Result Details</h1>
       <p>Show: {{ element.result }}</p>
       <table>
         <tr>
         <th>Venue Name</th>
         <th>Venue Place</th>
         <th>Venue Location</th>
         <th>Date</th>
         <th>Time</th>
         <th>Ticket Price</th>
         <th v-if="localstoragecheck('user')">Book Now</th>
      </tr>
      <tr  v-for="link in element.link" :key="link.id">
        <td>{{ link.venue_name }}</td>
        <td>{{ link.place }}</td>
        <td>{{ link.location }}</td>
        <td>{{ link.date }}</td>
        <td>{{ link.time }}</td>
        <td>{{ link.ticket_price }}</td>
        <td v-if="localstoragecheck('user')"><button class="btn btn-primary btn-sm" v-if="link.tickets_left>0" @click="book(link.link_id)">Book Now</button>
              <button class="btn btn-grey btn-sm" v-else disabled>Sold out</button></td>
      </tr>
       </table>
    </div>

  </template>
  
  <script>
export default {
  name: 'SearchResults',
  props: {
    element: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      selectedRating: null, // Store the selected rating filter
      selectedTags: [],     // Store the selected tags filter
      tags: ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Fiction'], // Sample array of available tags
    };
  },
  methods: {
    localstoragecheck(arg) {
      if (arg === 'user') {
        const val = this.$store.state.role;
        return val === 'user';
      }
    },
    book(id) {
      this.$router.push(`/book/${id}`);
    },
    // Function to get unique ratings from the links
    getAvailableRatings() {
      const ratings = new Set();
      //this.element.link.forEach((link) => ratings.add(link.rating));
      for(let i=1; i<=5; i++){ratings.add(i)}
      return ratings//Array.from(ratings);
    },
    removeFilter(){
    this.selectedRating = null;
    this.selectedTags = [];}
  },
  computed: {
    filteredLinks() {
      // Apply rating filter if selectedRating is not null
      let links = this.element.link;
      if (this.selectedRating) {
        links = links.filter((link) => link.rating >= this.selectedRating);
      }

      // Apply tags filter if selectedTags array is not empty
      if (this.selectedTags.length > 0) {
        links = links.filter((link) => link.tags === this.selectedTags);
      }

      return links;
    },
    availableRatings() {
      return this.getAvailableRatings();
    },
  }
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
th{
    background-color: #ccc;
}
</style>

  