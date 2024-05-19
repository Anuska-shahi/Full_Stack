<template>
    <div>
      <nav class="bg-blue-500">
        <div class="flex justify-evenly items-center  px-4 py-4">
          <div class="flex">
            <router-link to="/dashboard" class="text-white text-xl mx-20">My posts</router-link>
            <router-link to="/allblogs" class="text-white text-xl mx-20">Explore</router-link>
            <router-link to="/blog-create" class="text-white  text-xl mx-20">Create blog</router-link>
            <router-link to="/bin" class="text-white text-xl mx-20">Bin</router-link>
            <router-link to="/" class="text-white  text-xl mx-20">Logout</router-link>
          </div>
        </div>
      </nav>
      <div class="container mx-auto px-4 py-4 mt-14">
        <div class="grid grid-cols-1 gap-4 "> 
          <div v-for="blog in blogs">
            <div class="bg-white border border-blue-500 shadow-md rounded-lg p-6">
              <h2 class="text-5xl text-blue-500 mb-5">{{ blog.title }}</h2> 
              <p class="text-gray-600 mb-4 text-xl text-justify">{{ blog.Content }}</p> 
              <p class="text-gray-700 font-bold">Author: {{ blog.author_email }}</p>
              <p class="text-gray-700 ">Date: {{ blog.published_date }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
<script setup>
import axios from 'axios';
import { onMounted, ref,computed} from 'vue';
import { useRouter } from 'vue-router';
import {useToast} from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-sugar.css';

const toast=useToast({ position: 'bottom-left'});
const blogs = ref([]);
const router = useRouter();
const $toast = useToast();
const getPost = () => {
    return axios.get("http://127.0.0.1:8000/blogpost/blogs/?all=true",{ withCredentials: true })
        .then(response => {
            blogs.value = response.data;
        })
        .catch(error => {
            console.error(error);
        });

};
onMounted(getPost);
</script>