<template>

</template>
<script setup>
  import {onMounted,ref,onBeforeMount} from 'vue';
  import axios from 'axios';
  import {useToast} from 'vue-toast-notification';
  import 'vue-toast-notification/dist/theme-sugar.css';
  import { useRouter, useRoute} from 'vue-router'
  const router = useRouter();
  const route = useRoute();
  const userId=ref('');
  const $toast = useToast();
  const emits = defineEmits(['user-deleted']);
  const props = defineProps(['userIdToDelete']);
  const deleteUser = () => {
        axios.delete(`http://127.0.0.1:8000/accounts/users/${userId.value}/`)
        .then(response => {
            // alert('User deleted successfully:', response.data);
            $toast.success('User deleted successfully');
            router.push('/display-user')
        
        })
        .catch(error => {
            console.error('Error deleting user:', error);
            $toast.error("User delete unsuccessful",{ position: 'bottom-right'});
        });
  };
  onBeforeMount(() => {
  if (route.params.userId) {
    userId.value = route.params.userId;
  } else {
    console.error('User ID not provided in route params');
  }
});
  onMounted(deleteUser);
</script>
