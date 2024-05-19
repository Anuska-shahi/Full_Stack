<template>
    <div class="flex flex-row justify-center space-x-12">
        <div>
            <form @submit.prevent="submitForm()" class="border border-blue-500 rounded-lg p-12 space-y-9 mt-10">
                <div class="flex flex-col space-y-1">
                    <label for="first name">First Name</label>
                    <input type="text" name="fname" v-model="formData.fname" required class="border border-black w-96 h-10 rounded-lg">
                </div>

                <div class="flex flex-col space-y-1">
                    <label for="last name">Last Name</label>
                    <input type="text" name="lname" v-model="formData.lname" required class="border border-black w-96 h-10 rounded-lg">
                </div>

                <div class="flex flex-col space-y-1">
                    <label for="email">Email</label>
                    <input type="email" name="email" v-model="formData.email" required class="border border-black w-96 h-10 rounded-lg">
                </div>
                <div class="flex flex-col space-y-1">
                    <label for="address">Address</label>
                    <input type="text" name="address" v-model="formData.address" required class="border border-black w-96 h-10 rounded-lg">
                </div>
                <div class="flex flex-col space-y-1">
                    <label for="phone No">Phone No</label>
                    <input type="number" name="phone" v-model="formData.phone" required class="border border-black w-96 h-10 rounded-lg">
                    <span v-if="!isValidPhone" class="warning">{{ phoneWarning }}</span>
                </div>
                <div class="flex flex-col space-y-1">
                    <label for="password">Password</label>
                    <input type="password" name="password" v-model="formData.password"  required class="border border-black w-96 h-10 rounded-lg">
                    <span v-if="!isValidPassword" class="warning">{{ passwordWarning }}</span>
                </div>
                <div class="flex flex-col space-y-1">
                    <label for="confirm password">Confirm Password</label>
                    <input type="password" name="cpassword" v-model="formData.cpassword" min-length=8 required class="border border-black w-96 h-10 rounded-lg">
                </div>

                <div class="text-center">
                    <input type="submit" value="Register" class="border border-black w-32 h-10 bg-blue-500 text-white rounded-lg" >
                </div>
            </form>
        </div>
        <div class="">
            <img src="/home/anuska/vue-project/src/images/signup-image (1).jpg" class="">
        </div>
    </div>
</template>


<script setup>
    import { ref} from 'vue';
    import axios from 'axios';
    import {useToast} from 'vue-toast-notification';
    import 'vue-toast-notification/dist/theme-sugar.css';
    const $toast = useToast();
    const phoneWarning=ref('');
    const isValidPhone= ref(true);
    const passwordWarning=ref('');
    const isValidPassword= ref(true);
    const formData = ref({
        first_name: '',
        last_name: '',
        email: '',
        address: '',
        phone_no: '',
        password: '',
        cpassword: ''
    });
    const submitForm = () => {
        const password = formData.value.password;
        const phone = formData.value.phone.toString();;
        const passwordReg = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$/;
        if (phone.length!=10) {        
            isValidPhone.value = false;
            phoneWarning.value = 'Phone number should be 10 digits.';
            return
        } else {
            isValidPhone.value = true;
            phoneWarning.value = '';
        }
     

        if (!passwordReg.test(formData.value.password)) {
            isValidPassword.value = false;
            passwordWarning.value = "Must contain at least one uppercase letter, one lowercase letter, one special character, one number, and should be at least 8 characters long.";
            return
        }
        else {
            isValidPassword.value = true;
            passwordWarning.value = '';
        }

        if (formData.value.password !== formData.value.cpassword) {
            isValidPassword.value = false
            passwordWarning.value='Password and Confirm Password do not match.';
            return;
        }
        else{
            isValidPassword.value = true;
            passwordWarning.value='';
        }
        
            

        axios.post('http://127.0.0.1:8000/accounts/users/',{
            first_name: formData.value.fname,
            last_name: formData.value.lname,
            email: formData.value.email,
            address: formData.value.address,
            phone_no: formData.value.phone,
            password: formData.value.password
        })
        .then (response => {
            console.log('User registered:', response.data);
            $toast.success('User registered successfully');
        
            formData.value = {
                first_name: '',
                last_name: '',
                email: '',
                address: '',
                phone_no: '',
                password: '',
                cpassword: ''
            };

        })
        .catch(error=>{
            console.error('Error posting user data:', error);
            $toast.error("User registration unsuccessful",{ position: 'bottom-right'});
        });
      };
</script>
<style scoped>
</style>