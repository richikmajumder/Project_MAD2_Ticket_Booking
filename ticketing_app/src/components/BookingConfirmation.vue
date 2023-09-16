<template>
    
    <div class="booking-confirmation">
    <!-- Modal Trigger -->
    <button type="button" class="btn btn-primary" @click="openModal(show)">Book Now</button>

    <!-- Modal -->
    <div class="modal show" >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Booking Confirmation</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <p><strong>Show Name:</strong> {{ details.show_name }}</p>
            <p><strong>Venue Name:</strong> {{ details.venue_name }} {{ details.place }}, {{ details.location }}</p>
            <p v-if="details.surge===true" class="text-danger">High demand !!! Surge price applicable.</p>
            <p><strong>Price:</strong> ₹{{ details.ticket_price }}</p>
            <p><strong>Date:</strong> {{ details.date  }}</p>
            <p><strong>Time:</strong> {{ details.time }}</p>
            <p><strong>No of seats left:</strong>{{ details.tickets_left }}</p>
            <label for="no_of_seats_requested"><strong>No of seats:</strong></label>
            <select name="no_of_seats_requested" v-model.number="details.no_of_seats_requested" >
                <option v-for="num in Math.min(details.tickets_left,10)" :key="num" :value="num">{{ num }}</option>
            </select>
          </div>
          <div class="wallet-section">
          <p v-if="details.wallet > 0">
            <input type="checkbox" v-model="details.checked" name="wallet" value="true">
            <label for="wallet"  class="wallet">Use Wallet:₹{{ details.wallet }}</label>
          </p>
        </div>
          
          <div class="modal-footer">
            
            <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
            <button type="button" class="btn btn-primary" v-if="details.tickets_left>=1 && details.no_of_seats_requested" @click="confirmBooking('http://127.0.0.1:8080/api/book?id='+this.id,details)">Confirm Booking</button>
            <button type="button" class="btn btn-grey" v-else-if="details.tickets_left==0" @click="confirmBooking" disabled>Sold out</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import '../style.css';
import { update } from '../functions/update.js'
import { url } from '@/functions/url';
import { format } from 'date-fns';
import alertify from 'alertifyjs';
export default{
    name:'BookingConfirmation',
    data(){
        return{
            id:null,
            details:{
                id:null,
                show_name:'',
                venue_name:'',
                place:'',
                location:'',
                date:'',
                time:'',
                ticket_price:null,
                tickets_left:null,
                no_of_seats_requested:null,
                wallet:null,
                checked:false,
                price:null,
                surge:false

            }
        }
    
    },
    methods:{
        closeModal(){
            this.$router.push('/book')
        },
        confirmBooking(url,payload){
            const total = this.details.ticket_price*this.details.no_of_seats_requested;
            if(payload.checked){
              alertify.confirm('Are you sure?',`Your total amount is ₹${total}.          \n You are paying ₹${this.details.wallet} from your wallet and remaining ₹${Math.max(0,total-this.details.wallet)} from other payment method`,()=>update(url,payload,this.$router),()=>this.closeModal())
            }
            else{
              alertify.confirm('Are you sure?',`Your total amount is ₹${total}`,()=>{update(url,payload,this.$router);this.$router.push('/protected')},()=>this.closeModal())
            }
            
        }
    },
    mounted(){
        this.id = this.$route.params.id;
        fetch(`${url}api/book?id=${this.id}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('authToken')}`
        }
      }).then(response=>{
          if(response.ok){
              return response.json()
          }
          else{
              this.$router.push('/signin')
          }
      }).then(data=>{
          this.details.show_name = data.show_name;
          this.details.venue_name = data.venue_name;
          this.details.place = data.place;
          this.details.location = data.location;
          this.details.date = format(new Date(`${data.date} ${data.time}`),'EEE, dd-MMM');
          this.details.time = format(new Date(`${data.date} ${data.time}`),'hh:mm a');
          this.details.ticket_price = data.ticket_price;
          this.details.tickets_left = data.tickets_left;
          this.details.id = data.id;
          this.details.wallet = data.wallet;
          this.details.price = data.price;
          if(data.price!=data.ticket_price){
            this.details.surge=true;
            setTimeout(()=>{this.details.surge=false},10000)
          }


      }).catch(error=>{console.log(error);
        //this.$router.push('/signin')
      })
    },
}

</script>
<style scoped>
.booking-confirmation {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.modal {
  display: none;
  position: fixed;
  z-index: 1000;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal.show {
  display: block;
}

.modal-dialog {
  max-width: 400px;
  margin: 1.75rem auto;
}

.modal-content {
  padding: 1rem;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  margin: 0;
}

.modal-body {
  margin-bottom: 1rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
}

.wallet-section {
  display: flex;
  align-items: left;
}

.wallet-section input[type="checkbox"] {
  width:40px
  
}

.wallet{
  width:200px;
}
</style>