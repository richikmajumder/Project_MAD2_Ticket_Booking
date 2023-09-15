<template>
    <div class="modal">
   <center>
                <div class="modal-content">
                <span class="close" @click="closeForm">&times;</span>
                <h2>Booking History</h2>
                <!-- Add your form fields and submit button here -->
                <table>
                    <tr>
                        <th>Venue Name</th>
                        <th>Venue Place</th>
                        <th>Venue Location</th>
                        <th>Show Name</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>No of tickets booked</th>
                        <th>Ticket Price</th>
                        <th>Rate now</th>
                    </tr>
                    <tr v-for="link in links" :key="link.id">
                        <td>{{ link.venue_name }}</td>
                        <td>{{ link.place }}</td>
                        <td>{{ link.location }}</td>
                        <td>{{ link.show_name }}</td>
                        <td>{{ link.date }}</td>
                        <td>{{ link.time }}</td>
                        <td>{{ link.tickets_booked }}</td>
                        <td>{{ link.ticket_price }}</td>
                        <td><button class="btn btn-primary btn-sm" v-if="link.rating===null" @click="openrating(link)">Rate Now</button>
                        <a>{{ link.rating }}</a></td>
                        <RateNow :show_id=link.show_id :user_id=link.user_id v-if="link.modifier" @close="closerating(link)"></RateNow>
                    </tr>
                </table>
                
              </div>
    </center>
   

</div> 
</template>

<script>
import '../style.css'
import { get } from '@/functions/get'
import { url } from '@/functions/url'
import RateNow from '../components/RateNow.vue'
export default{
    name:'BookingHistory',
    props:{username:{
        type:String,
        required:true
    }},
    components:{RateNow},
    data(){
        return{
            links:null,

        }
    },
    methods:{
        closeForm(){
            this.$emit('close')
        },

        openrating(data){
        data.modifier=true;       
    },
        closerating(data){
            data.modifier=false;
            location.reload();
        }
    },
    created(){
        get(`${url}api/bookinghistory?id=${this.username}`).then(data=>this.links=data)

    },
    
}

</script>
<style scoped>
.modal{
display: flex;

}
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