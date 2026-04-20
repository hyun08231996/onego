import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Main from '@/views/Main.vue'
import SearchResult from '@/views/SearchResult.vue'
import Scrap from '@/views/Scrap.vue'
import Article from '@/views/Article.vue'
import Setting from '@/views/Setting.vue'
import ChangePassword from '@/views/ChangePassword.vue'
import EditProfile from '@/views/EditProfile.vue'
import MyOnego from '@/views/MyOnego.vue'
import MyProfile from '@/views/MyProfile.vue'
import UserProfile from '@/views/UserProfile.vue'
import SignUpPage from '@/views/SignupPage.vue'
import LoginPage from '@/views/LoginPage.vue'
import ForgotPassword from '@/views/ForgotPasswordPage.vue'
import Write from '@/views/Write.vue'
import Content from '@/views/Content.vue'
import FollowingList from '@/views/FollowingList.vue'
import FollowerList from '@/views/FollowerList.vue'
import { Auth } from 'aws-amplify'
Vue.use(VueRouter)

const requireAuth = () => (to: any, from: any, next: any) => {

	Auth.currentAuthenticatedUser()
		.then(user => {
			if (user) {
				next();
			}
		})
		.catch(err => {
			console.log(err)
			next('/login')

		});
}

const routes: Array<RouteConfig> = [
	{
		path: "/",
		name: "Main",
		component: Main,
		meta:{ showFooter: true, showHeader: true }
	},
	{
		path: "/signup",
		name: "signup",
		component: SignUpPage,
		meta: { showFooter: false, showHeader: true }
	},
	{
		path: "/login",
		name: "login",
		component: LoginPage,
		meta: { showFooter: false, showHeader: true },
		props: true
	},
	{
		path: "/search/:search",
		name: "SearchResult",
		component: SearchResult,
		props: true,
		meta:{ showFooter: true}
	},
	{
		path: "/scrap",
		component: Scrap,
		meta:{ showFooter: true, showHeader: true },
		beforeEnter: requireAuth()
	},
	{
		path: "/article",
		component: Article,
		meta:{ showFooter: true, showHeader: true },
	},
	{
		path: "/setting",
		name: "Setting",
		component: Setting,
		meta:{ showFooter: true, showHeader: true },
		beforeEnter: requireAuth()
	},
	{
		path:"/change-pass",
		name: "ChangePassword",
		component: ChangePassword,
		meta:{ showFooter: true, showHeader: true },
		beforeEnter: requireAuth()
	},
	{
		path:"/forgotPassword",
		name: "ForgotPassword",
		component: ForgotPassword,
	},
	{
		path:"/edit-prof",
		name: "EditProfile",
		component: EditProfile,
		meta:{ showFooter: true, showHeader: true },
		beforeEnter: requireAuth()
	},
	{
		path:"/myonego",
		name: "MyOnego",
		component: MyOnego,
		meta:{ showFooter: true, showHeader: true },
		beforeEnter: requireAuth()
	},
	{
		path:"/myprofile",
		name: "MyProfile",
		component: MyProfile,
		props: true,
		meta: {
			headerClass: 'myprof-header-color',
			showFooter: true, showHeader: true
		},
		beforeEnter: requireAuth()
	},
	{
		path:"/userprofile",
		name: "UserProfile",
		component: UserProfile,
		props: true,
		meta:{
			headerClass: 'myprof-header-color',
			showFooter: true, showHeader: true
		},
		beforeEnter: requireAuth()
	},
	{
		path:"/write",
		name: "Write",
		component: Write,
		meta:{ showFooter: false, showHeader: false, showEdit: false  },
		beforeEnter: requireAuth()
	},
	{
		path:"/write/:tempBoardId",
		name: "WriteEdit",
		component: Write,
		props:true,
		meta:{ showFooter: false, showHeader: false, showEdit: false },
		beforeEnter: requireAuth()
	},
	{
		path:"/write/post/:boardId",
		name: "PostEdit",
		component: Write,
		props:true,
		meta:{ showFooter: false, showHeader: false, showEdit: true },
		beforeEnter: requireAuth()
	},
	{
		path:"/content/:boardId",
		name: "Content",
		meta:{ showScrap: true },
		props:true,
		component: Content,
	},
	{
		path:"/following",
		name: "Following",
		props: true,
		component: FollowingList,
		beforeEnter: requireAuth()
	},
	{
		path:"/follower",
		name: "Follower",
		props: true,
		component: FollowerList,
		beforeEnter: requireAuth()
	}
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router