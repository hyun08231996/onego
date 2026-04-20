<template>
  <v-app >
	<Header :class="$route.meta.headerClass"/>
	<router-view id="content-margin"/>
	<Footer v-if="$route.meta.showFooter"/>
  </v-app>
</template>

<script lang="ts">
	import Vue from 'vue'
	import Header from '@/components/layout/Header.vue'
	import Footer from '@/components/layout/Footer.vue'
	import http from '@/http/http-common'

	export default Vue.extend({
		name: "App",
		components:{
			Header, Footer
		},
		methods: {
			async bootstrapAuth() {
				await this.$store.dispatch('findUser');

				const signedIn = this.$store.state.user.signedIn;
				const userInfo = localStorage.getItem('userInfo');
				const accessToken = localStorage.getItem('accessToken');
				const email = this.$store.state.user.userAccount?.attributes?.email;

				if (signedIn && !userInfo && accessToken && email) {
					try {
						const response = await http.get('/users/' + email, {
							headers: {
								Authorization: 'Bearer ' + accessToken
							}
						});
						this.$store.commit('setUserInfo', response.data);
						localStorage.setItem('userInfo', JSON.stringify(response.data));
					} catch (error) {
						console.log('failed to restore user info', error);
					}
				}
			}
		},
		async created(){
			await this.bootstrapAuth();
		},
	})
</script>


<style lang ="scss">
	#app {
		font-family: 'Nanum Myeongjo', serif !important;
	}
	#content-margin{
		margin-top:100px;
		margin-bottom:400px;
	}
	.v-avatar img {
		object-fit: cover;
		object-position: center;
	}
</style>
