<template>
    <div class="table-container">
      
      <table>
        <caption>User List</caption>
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
            <button @click="restoreUser(user.id)" class="edit">Restore</button>
            <button @click="removeUser(user.id)" class="delete">Remove</button>
          </td>
        </tr>
      </table>
    </div>
  </template>
  
  <script setup>
    import { ref, onMounted} from 'vue';
    import axios from 'axios';
    import {useToast} from 'vue-toast-notification';
    import 'vue-toast-notification/dist/theme-sugar.css';
    const $toast = useToast();
    const users = ref([]);
    const getUsers = () => {
        axios.get('http://127.0.0.1:8000/accounts/users/?deleted=true')
        .then (response => {
          users.value = response.data;
        })
        .catch(error=>{
            console.error('Error fetching users:', error);
        });
      };
      onMounted(getUsers);

      const removeUser = (userId) => {
        axios.delete(`http://127.0.0.1:8000/accounts/users/${userId}/hard-delete/`)
        .then(response => {
            // alert('User deleted successfully:', response.data);
            $toast.success('User permantenetly deleted');
            getUsers()
        })
        .catch(error => {
            console.error('Error deleting user:', error);
            $toast.error("User deletion unsuccessful",{ position: 'bottom-right'});
        });
      };
      const restoreUser = (userId) => {
        axios.post(`http://127.0.0.1:8000/accounts/users/${userId}/restore/`)
        .then(response => {
            // alert('User restored successfully:', response.data);
            $toast.success('User restore successfully');
            getUsers();
        })
        .catch(error => {
            console.error('Error restoring user:', error);
            $toast.error("User restore unsuccessful",{ position: 'bottom-right'});
        });
      };
      </script>
<style scoped>
table,th,td{
  border: 1px solid black;
  /* border-collapse: collapse; */
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
}th{
    background-color: #f4939a;
  }

</style>
  