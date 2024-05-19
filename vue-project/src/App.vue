<template>
  

  <router-view></router-view>
  <!-- <div >
    <button @click="showDisplay">Display</button>
    <button @click="showAdd">Add</button>
    <button @click="showTrash">Trash</button>
  </div>
  <br/>

  <div v-if="currentTab === 'display'">
    <Display @delete-user="handleDeleteUser" @edit-user="handleEditUser" :refreshUser="refresh" ></display>
    <span v-if="userIdToDelete!==null">
      <Delete :userIdToDelete="userIdToDelete" @user-deleted="handleUserDeleted"/>
    </span>
    <span v-if="userIdToEdit!==null">
      <EditForm :userIdToEdit="userIdToEdit"/>
    </span>
    
  </div>
  <div v-else-if="currentTab === 'add'">
    <RegisterForm></RegisterForm>
  </div>
  <div v-else-if="currentTab === 'deleteUser'">
    <DisplayDeleted></DisplayDeleted>
  </div>
  <div v-else-if="currentTab === ''">
    <login></login> 
  </div> 
  -->
 
</template>

<script setup>
  // import RegisterForm from './components/RegisterForm.vue'
  // import Display from './components/Display.vue'
  // import Delete from './components/Delete.vue'
  // import EditForm from './components/EditForm.vue'
  // import DisplayDeleted from './components/DisplayDeleted.vue'
  // import login from './components/Login.vue'
 
  // import {ref} from 'vue'
  // const currentTab = ref('');
  // const userIdToDelete = ref(null);
  // const userIdToEdit = ref(null);
  // const refresh = ref(null);
  
  // const showDisplay = () => {
  //   currentTab.value = 'display'
  // };

  // const showAdd = () => {
  //   currentTab.value = 'add';
  // };
  // const showTrash= () => {
  //   currentTab.value = 'deleteUser';
  // };
  // const handleDeleteUser = (userId) => {
  //   userIdToDelete.value = userId;
  // };
  // const handleEditUser = (user) => {
  //   userIdToEdit.value = user;

  // };
  
  // const handleUserDeleted = () => {
  //   currentTab.value = 'display';
  //   console.log("hello")

  //   console.log("hello world")
  //   userIdToDelete.value = null;
  //   if (currentTab.value === 'display') {
  //     showDisplay();
  //     console.log("inside") // This will trigger the display component to refresh the user list
  //   }
  // };
  // const refreshUsers = () => {
  //   refresh.value='refresh';
  // };

</script>

<style scoped>
  /* button{
    margin: 15px;
    width: 80px;
    height: 50px;
    color: white;
    background-color: cadetblue;

  } */
</style>
