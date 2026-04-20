<template>
  <div>
	<v-flex id="myprof-margin" class="mx-auto">
	  <div align="center" class="spacing">
		<div class="image-container">
			<img src="@/assets/images/beach.jpg" width="100%" height="auto">
			<v-list-item-avatar id="prof-pic" absolute elevation="4" size=100>
				<img :src="user.profileImage">
			</v-list-item-avatar>
			<v-btn id="myprof-write-btn" @click="changeState, subscribe(user.email)" absolute rounded outlined color="#00d5aa" >
				구독
			</v-btn>

		</div>
	  </div>
	  <div class="spacing">
		  <div><label style="font-size:1.4em;font-weight:bold;">{{user.nickName}}</label></div>
		  <div><label style="font-size:0.95em;opacity:75%;">{{user.intro}}</label></div>
	  </div>
	  <div class="spacing">
	    <div class="follow">
		  <a href='#' id="follower-hover">
			<div>
		    <div><label class="label label-follow" style="font-size:0.80em;opacity:60%;">구독자</label></div>
		    <div><label class="label label-number" style="font-size:1.2em;opacity:55%;">{{user.followers.length}}</label></div>
			</div>
		  </a>
		</div>
		<div class="follow" style="margin-left:50px;">
		  <a href='#' id="following-hover">
			<div>
		    <div><label class="label label-follow" style="font-size:0.80em;opacity:60%;">관심 작가</label></div>
		    <div><label class="label label-number" style="font-size:1.2em;opacity:55%;">{{user.followings.length}}</label></div>
			</div>
		  </a>
	    </div>
	  </div>
	  <div style="margin-top:40px;padding-top:25px;padding-bottom:10px;background-color:#FAFAFA;">
	  	<p style="opacity:55%;margin-left:30px;font-size:1.1em;"><em><strong>커서가 깜빡이는 순간, 당신은 이미 작가입니다.</strong></em></p>
	 	<p style="opacity:55%;margin-left:30px;font-size:1.1em;"><em><strong>ONEGO에서는 작가님을 응원합니다.</strong></em></p>
	  </div>
	</v-flex>
  </div>
</template>

<script lang="ts">
	import Vue from 'vue'
	import http from '../http/http-common'

	export default Vue.extend({
		props: {
			emailProp: {
				type: String,
				default: "",
			}
		},
		data: () => ({
			user:{
				name:'원고', nickname:'원고팀', email:'onego@gmail.com',
				intro:'원고',
				pic:"https://randomuser.me/api/portraits/women/82.jpg",
				followers:'100', following:'0'
			},
			email: '',
			disabledFollowing:false,
			disabledFollower:false
		}),
		methods:{
			changeState(){
				// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
				var clicked = document.getElementById('myprof-write-btn')!;
				if(clicked.innerText=='구독'){
					clicked.innerText = '구독중';
					clicked.style.fontWeight = 'bold';
					clicked.style.backgroundColor = '#00d5aa';
					clicked.style.color = 'white';
					clicked.style.borderColor = 'white';
				}else{
					clicked.innerText = '구독';
					clicked.style.backgroundColor = 'white';
					clicked.style.color = '#00d5aa';
					clicked.style.borderColor = '#00d5aa';
				}
			},
		},
		async created(){
			if(this.user.following == '0'){
				this.disabledFollowing = true;
			}
			if(this.user.followers == '0'){
				this.disabledFollower = true;
			}
			this.email = this.emailProp

			await http
				.get('/users/'+this.email)
				.then(response => {
					this.user = response.data

				})
		}
	})
</script>

<style>
.v-application .myprof-header-color .white{
	background-color:transparent !important;
}
#myprof-margin{
	max-width:55%;
	margin-top: -100px;
}
.spacing{
	margin-bottom:30px;
}
#following-hover,
#follower-hover{
	text-decoration: none !important;
	color: black !important;
}
#myprof-write-btn:hover{
	color:#02bf99 !important;
}
.image-container{
	position:relative;
}
.image-container img{
	display:block;
}
.image-container #prof-pic{
	position:absolute;
	bottom:-55px;
	right:20px;
}
.image-container #myprof-write-btn{
	position:absolute;
	bottom:-150px;
	right:20px;
}
.follow{
	float:left;
}
#follower-hover:hover .label,
#following-hover:hover .label{
	cursor:pointer !important;
}
#follower-hover:hover .label-follow,
#following-hover:hover .label-follow{
	color:black !important;
}
#follower-hover:hover .label-number,
#following-hover:hover .label-number{
	text-decoration:underline;
	color:#00d5aa;
}
</style>