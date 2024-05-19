<template>
    <div>
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
      <div class="container mx-auto px-4 py-4 mt-14">
        <div class="grid grid-cols-1 gap-4"> 
            <div v-for="blog in blogs">
                <div class="bg-white border border-blue-500shadow-md rounded-lg p-6">
                    <h2 class="text-5xl text-blue-500 mb-5">{{ blog.title }}</h2> 
                    <p class="text-gray-700 ">Date: {{ blog.published_date }}</p>
                    <p class="text-gray-600 mb-4 text-xl text-justify">{{ blog.Content }}</p> 
                    <div class="flex flex-row-reverse">
                        <button class="ring-2 ring-blue-500 rounded-lg text-xl py-2 px-5" @click="deletePost(blog.id)">Delete</button>
                        <button class="ring-2 ring-blue-500 rounded-lg mr-11 text-xl py-2 px-5" @click="updatePost(blog.id)">Update</button>
                    </div>

                </div>
            </div>
            
        </div>
      </div>
    </div>
  </template>
<script setup>
import { useRouter } from 'vue-router';
import axios from 'axios';
import { onMounted, ref} from 'vue';
import {useToast} from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-sugar.css';

const toast=useToast({ position: 'bottom-left'});
const blogs = ref([]);
const router = useRouter();
const $toast = useToast();
const getPost = () => {
    return axios.get("http://127.0.0.1:8000/blogpost/blogs/",{ withCredentials: true })
        .then(response => {
            blogs.value = response.data;
        })
        .catch(error => {
            console.error(error);
        });

};
onMounted(getPost);
const deletePost = (blogId) => {
    axios.delete(`http://127.0.0.1:8000/blogpost/blogs/${blogId}/`,{ withCredentials: true })
        .then(response => {
            $toast.success('Blog post deleted successfully.');
            router.push('/dashboard')
        })
        .catch(error => {
            console.error('Error deleting user:', error);
            $toast.error("User delete unsuccessful",{ position: 'bottom-right'});
        });
    };
const updatePost=(blogId)=>{
      router.push({name:'UpdateBlog', params:{blogId:blogId}});
  }
</script>
