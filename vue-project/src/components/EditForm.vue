<template>
    <form @submit.prevent="updateForm">
        <div >
            <label for="id">Id</label>
            <input type="text" name="fname" v-model="formData.id" disabled>
        </div>
        <div >
            <label for="first name">First Name</label>
            <input type="text" name="fname" v-model="formData.first_name">
        </div>

        <div>
            <label for="last name">Last Name</label>
            <input type="text" name="lname" v-model="formData.last_name">
        </div>

        <div>
            <label for="email">Email</label>
            <input type="email" name="email" v-model="formData.email">
        </div>
        <div>
            <label for="address">Address</label>
            <input type="text" name="address" v-model="formData.address">
            
        </div>
        <div>
            <label for="phone No">Phone No</label>
            <input type="number" name="phone" v-model="formData.phone_no">
            <span v-if="!isValidPhone" class="warning">{{ phoneWarning }}</span>
        </div>
        <div>
            <input type="submit" value="Update">
        </div>
    </form>
    
    
</template>
<script setup>
    import { ref,onMounted,onBeforeMount} from 'vue';
    import axios from 'axios';
    import { useRouter,useRoute } from 'vue-router';
    import {useToast} from 'vue-toast-notification';
    import 'vue-toast-notification/dist/theme-sugar.css';

    const router = useRouter();
    const route = useRoute();
    const $toast = useToast();
    const phoneWarning=ref('');
    const isValidPhone= ref(true);
    // const props = defineProps(['userIdToEdit']);
    const userId = ref(route.params.userId);
    const users= ref()
    const formData = {
        id: '',
        first_name: '',
        last_name: '',
        email: '',
        address: '',
        phone_no: '',
    };
    const getUsers = () => {
        axios.get(`http://127.0.0.1:8000/accounts/users/${userId.value}/`)
        .then (response => {
            users.value = response.data;
            formData.value = {
                id: users.value.id,
                first_name: users.value.first_name,
                last_name: users.value.last_name,
                email: users.value.email,
                address: users.value.address,
                phone_no: users.value.phone_no
            };
        })
        .catch(error=>{
            console.error('Error fetching users:', error);
        });
      };
      onBeforeMount(getUsers);
        // const updateForm = () => {
        // const phone = formData.value.phone_no.toString();;
        // if (phone.length!=10) {        
        //     isValidPhone.value = false;
        //     phoneWarning.value = 'Phone number should be 10 digits.';
        //     return
        // } else {
        //     isValidPhone.value = true;
        //     phoneWarning.value = '';
        // }
        
        // axios.patch(`http://127.0.0.1:8000/accounts/users/${props.userIdToEdit.id}/`, {
        //     first_name: formData.value.first_name,
        //     last_name: formData.value.last_name,
        //     email: formData.value.email,
        //     address: formData.value.address,
        //     phone_no: formData.value.phone_no,
        //  })
        // .then (response => {
        //     let instance = $toast.success('User Updated successfully');
        
        //     console.log('User registered:', response.data);
        //     formData.value = {
        //         first_name: '',
        //         last_name: '',
        //         email: '',
        //         address: '',
        //         phone_no: '',
        //     };
        // })
        // .catch(error=>{
        //     console.error('Error posting user data:', error);
        //     $toast.error("User update unsuccessful",{ position: 'bottom-right'});
 
        // });
    //   };
</script>
<style scoped>
    form{
        border: 1px solid black;
        width: min-content;
        padding: 50px;
        font-size: 25px;
        margin: auto;
    }
    div{
        margin:10px;
    }
    input{
        width:500px;
        height: 50px;
        font-size:30px;
        margin: 10px 0;
    }
    input[type=submit]{
        background-color: cadetblue;
        border: none;
        color: white;
        padding: 0;
        height: 50px;
        width: 200px;
        margin: 4px 2px;
    }
    .warning{
        color: red;
        font-size: 20px;
    }
    
</style>