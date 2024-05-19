import{createWebHistory,createRouter} from 'vue-router';
import RegisterForm from './components/RegisterForm.vue'
import Display from './components/Display.vue'
import Delete from './components/Delete.vue'
import EditForm from './components/EditForm.vue'
import DisplayDeleted from './components/DisplayDeleted.vue'
import Login from './components/Login.vue';
import Dashboard from './components/Dashboard.vue';
import AllBlogs from './components/AllBlogs.vue';
import CreateBlog from './components/CreateBlog.vue';
import Bin from './components/Bin.vue';
import UpdateBlog from './components/UpdateBlog.vue';
const routes=[
    {
        name:'RegisterForm',
        path:'/Signup',
        component:RegisterForm
    },
    {
        name:'Display',
        path:'/display-user',
        component:Display
    },
    {
        name:'Delete',
        path:'/delete-user/:userId',
        component:Delete,
    },
    {
        name:'Dashboard',
        path:'/dashboard',
        component:Dashboard
    },
    {
        name:'AllBlogs',
        path:'/allblogs',
        component:AllBlogs
    },
    {
        name:'CreateBlog',
        path:'/blog-create',
        component:CreateBlog
    },
    {
        name:'UpdateBlog',
        path:'/blog-update/:blogId',
        component:UpdateBlog
    },
    {
        name:'Bin',
        path:'/bin',
        component:Bin
    },
    {
        name:'EditForm',
        path:'/edit-user/:userId',
        component:EditForm,
    },
    {
        name:'DisplayDeleted',
        path:'/Display-deleted',
        component:DisplayDeleted
    },
    {
        name:'Login',
        path:'/',
        component:Login
    },
];
const router=createRouter({
    history:createWebHistory(),
    routes
});
export default router;