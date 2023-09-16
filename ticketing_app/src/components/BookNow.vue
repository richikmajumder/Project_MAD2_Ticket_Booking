<template>
  <div class="book-now-container">
    <div class="row row-cols-1 row-cols-md-4">
     
      <div class="col mb-4" v-for="x in filteredlist" :key="x.id">
        <!-- Card -->
        <div class="card h-100 shadow-sm" >

          <!-- Card content -->
          <div class="card-body">

            <!-- Title -->
            <h4 class="card-title text-center">{{ x.name }} {{ x.place }}, {{ x.location }}</h4>

            <!-- Show details -->
            <ul class="list-unstyled mb-3">
              <li v-for="link in x.links" :key="link.id">
                <div class="d-flex justify-content-between align-items-center">
                  <span class="fw-bold">{{ link.show_name }}</span>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                  <span>{{ link.datetime }}</span>
                  <span>₹{{ link.ticket_price }}</span>
                </div>
                <div class="text-end mt-3">
                  <button href="#" class="btn btn-primary btn-sm" v-if="link.tickets_left >= 1" @click="confirmation(link.id)">Book Now</button>
                  <button href="#" class="btn btn-grey btn-sm" v-else disabled>Sold out</button>
                </div>
                <hr class="my-3"> <!-- Line separator -->
              </li>
            </ul>

          </div>

        </div>
        <!-- Card -->

      </div>
    </div>
    <a href="/protected" class="back-link">Back</a>
  </div>
</template>

<script>
import { get } from '../functions/get.js'
import { url } from '@/functions/url'
import { format } from 'date-fns'
export default {
  name: 'BookNow',
  data() {
    return {
      list: [],
      username: '',
      email: ''
    }
  },
  methods: {
    confirmation(id) {
      this.$router.push(`/book/${id}`)
    }
  },
  mounted() {
    fetch(`${url}user/protected`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('authToken')}`
          }
        })
        .then(response => {
          // Check if the response status is 200 (OK)
          if (response.ok) {
            this.$store.commit('role','user');
            get(`${url}api/book`).then(res =>{
                this.list = res;
                return res})
                .then(res=>
                {for(let i=0;i<res.length;i++){
        for(let j=0;j<res[i].links.length;j++){
          this.list[i].links[j].datetime=format(new Date(`${res[i].links[j].date} ${res[i].links[j].time.slice(0,-3)}`), 'EEE, dd-MMM | hh:mm a')
          //console.log(format(new Date(res[i].links[j].time.slice(0,-3)), 'hh:mm a'))
        }
      }
      console.log(this.list);
    
    });
            return response.json();
          } else {
            //throw new Error('Unauthorized');
            localStorage.removeItem('authToken');
            this.$store.commit('role',null);
            this.$router.push('/signin');
            //alert('Logged out successfully \n Redirecting to sign in page.')
          }
        })
    
  },
  computed:{
    filteredlist(){
      return this.list.filter(item=>item.links.length>=1)
    }

  }
}
</script>

<style scoped>
.book-now-container {
  padding: 20px;
}

.card.h-100 {
  border: 1px solid #ccc;
  border-radius: 10px;
}

.card-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 15px;
}

ul.list-unstyled {
  margin: 0;
  padding: 0;
}

li {
  margin-bottom: 20px;
}

.btn-primary,
.btn-grey {
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.btn-grey {
  background-color: #ccc;
  color: #000;
}

.btn-primary:hover,
.btn-grey:hover {
  background-color: #0056b3;
}

hr.my-3 {
  border-top: 1px solid #ccc;
}

.back-link {
  display: block;
  text-align: center;
  margin-top: 20px;
  color: #007bff;
  text-decoration: none;
  font-weight: bold;
}
</style>
