<template>
   <div class="flex flex-row justify-center mt-48 space-x-12" >
        <div class="w-3/12 text-xl">
            
            <form @submit.prevent="submitForm()" class="border border-blue-500 rounded-lg p-12 space-y-9">
                <h1 class=" text-center text-2xl font-bold">Login</h1>
            <div  class="flex flex-col space-y-1">
                <label for="email">Email</label>
                <input type="email" name="email" v-model="formData.email" required  class="border border-black w-96 h-10">
            </div>
            <div class="flex flex-col space-y-1">
                <label for="password">Password</label>
                <input type="password" name="password" v-model="formData.password " class="border border-black w-96 h-10"  required>
                
            </div>
            <div class=" text-center text-blue-700"><router-link to="/signup">Create an account</router-link></div>

            <div class=" text-center">
                <input type="submit" value="Log in" class="border border-black w-32 h-10 bg-blue-500 text-white rounded-lg" >
            </div>
            </form>
        </div>
        <div class="flex-shrink-0 self-center ..." >
            <img src="/home/anuska/vue-project/src/images/signin-image.jpg">
        </div>
    </div>
    
</template>
<script setup>
    import { ref} from 'vue';
    import axios from 'axios';
    import {useToast} from 'vue-toast-notification';
    import { useRouter,useRoute } from 'vue-router'
    import 'vue-toast-notification/dist/theme-sugar.css';
    const $toast = useToast();
    const formData = ref({
        email: '',
        password: '',
    });
    const router = useRouter();
    const submitForm = () => {
        axios.post('http://127.0.0.1:8000/accounts/login/',{
            email: formData.value.email,
            password: formData.value.password },
            { withCredentials: true })
        .then (response => {
            console.log('Login sucessful:', response.data);
            // $toast.success('Login  successfully');
            router.push({name:'Dashboard'})
        
            formData.value = {
                email: '',
                password: '',
            };

        })
        .catch(error=>{
            console.error('Invalid email or password:', error);
            $toast.error("Invalid email or password",{ position: 'bottom-right'});
        });
      };
</script>
