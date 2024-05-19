<template>
    <nav class="bg-blue-500">
        <div class="flex justify-evenly items-center px-4 py-4">
          <div class="flex">
            <router-link to="/dashboard" class="text-white text-xl mx-20">My posts</router-link>
            <router-link to="/allblogs" class="text-white text-xl mx-20">Explore</router-link>
            <router-link to="/blog-create" class="text-white text-xl mx-20">Create blog</router-link>
            <router-link to="/bin" class="text-white text-xl mx-20">Bin</router-link>
            <router-link to="/" class="text-white text-xl mx-20">Logout</router-link>
          </div>
        </div>
      </nav>
    <div class="flex flex-row justify-center mt-40 space-x-12" >
         <div class="w-3/12 text-xl">
             
             <form @submit.prevent="submitForm()" class="border border-blue-500 rounded-lg p-12 space-y-9">
                 <h1 class=" text-center text-2xl font-bold">Create Blog</h1>
             <div  class="flex flex-col space-y-1">
                 <label for="title">Title</label>
                 <input type="text" name="title" v-model="formData.title" required  class="border border-black w-96 h-10">
             </div>
             <div class="flex flex-col space-y-1">
                 <label for="description">Description</label>
                 <textarea name="description" v-model="formData.content" class="border border-black w-96 h-52"></textarea>
                 
             </div>
             <div class=" text-center">
                 <input type="submit" value="Post" class="border border-black w-32 h-10 bg-blue-500 text-white rounded-lg" >
             </div>
             </form>
         </div>
         <div class="flex-shrink-0 self-center ..." >
             <img src="/home/anuska/vue-project/src/images/signin-image.jpg">
         </div>
     </div>
     
 </template>
 <script setup>
     import axios from 'axios';
     import {ref} from 'vue';
    import {useToast} from 'vue-toast-notification';
    import 'vue-toast-notification/dist/theme-sugar.css';
    import { useRouter, useRoute} from 'vue-router'
    const formData = ref({
        title: '',
        content: '',
    });
    const router = useRouter();
    const $toast = useToast();
    const submitForm = () => {
        axios.post('http://127.0.0.1:8000/blogpost/blogs/',{
            title: formData.value.title,
            content: formData.value.content
        },{ withCredentials: true })
        .then (response => {
            $toast.success('Blog created successfully');
        
            formData.value = {
                title: '',
                content: ''
            };
            router.push('/dashboard')

        })
        .catch(error=>{
            $toast.error("Blog create unsuccessful",{ position: 'bottom-right'});
        });
      };
</script>