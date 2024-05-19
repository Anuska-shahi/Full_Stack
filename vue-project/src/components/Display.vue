<template>
    <div class="table-container">
      
      <table>
        <caption>Users List</caption>
        <tr>
          <th>Id</th>
          <th>First Name</th>
          <th>Last Name</th>
          <th>Email</th>
          <th>Address</th>
          <th>Phone No.</th>
          <th>Action</th>
        </tr>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.first_name }}</td>
          <td>{{ user.last_name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.address }}</td>
          <td>{{ user.phone_no }}</td>
          <td>
            <button @click="editUser(user.id)" class="edit">Edit</button>
            <button @click="deleteUser(user.id)" class="delete">Delete</button>
          </td>
        </tr>
      </table>
    </div>
  </template>
  
  <script setup>
    import { ref, onMounted, defineEmits,watchEffect} from 'vue';
    import axios from 'axios';
    import { useRouter } from 'vue-router'
    const users = ref([]);
    const router = useRouter()
    const emits = defineEmits(['deleteUser']);
    const getUsers = () => {
        axios.get('http://127.0.0.1:8000/accounts/users/')
        .then (response => {
          users.value = response.data;
        })
        .catch(error=>{
            console.error('Error fetching users:', error);
        });
      };
      onMounted(getUsers);

      const deleteUser = (userId) => {
        emits('deleteUser', userId);
        router.push({name:'Delete', params:{userId:userId}})
      };
      const editUser = (userId) => {
        // emits('editUser', userId);
        router.push({name:'EditForm', params:{userId:userId}})
      };
      const handleDeleteUser = (userId) => {
         getUsers();
      }
      // Catch the event emitted when a user is deleted
      // const handleUserDeleted = () => {
      //   console.log("fetch");
      //   getUsers(); // Fetch the updated list of users
      // };
      // // Listen for the 'user-deleted' event emitted by the 'delete.vue' component
      // const onUserDeleted = () => {
      //   window.addEventListener('user-deleted', handleUserDeleted);
      //   console.log("del fetch");
      // };
    //   // onMounted(onUserDeleted);
    //   const refreshUsers = () => {
    //     getUsers();
    //   };
    //   watchEffect(() => {
    //   emits('refresh-users'); // Emit 'refresh-users' event whenever there's a reactive change
    // });
      </script>
      
<style scoped>
  table,th,td{
    border: 1px solid black;
    border-collapse: collapse;
    font-size: 25px;
  }
  table{
    width: 100%;
    border-radius: 10px;
    
  }
  td,tr{
    height: 60px;
  }
  td{
    text-align: center;
    background-color: #ffffff;
  }
  button{
    width:80px;
    height:35px;
    font-size: 18px;
    margin-right: 15px;
    border-radius: 12px;
    color: white;
  }
  .table-container{
    margin: 10px 30px;
  }
  .edit{
    background-color: #0CA3CE;
  }
  .delete{
    background-color: #BD2105;
  }
  th{
    background-color: #f4939a;
  }
  caption{
    font-weight: bold;
    font-size: 40px;
  }

</style>
  