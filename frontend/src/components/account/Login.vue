<template>
    <v-card-text>
        <p class="text-h4 text--primary">LOGIN</p><br>
        <v-text-field ref="email" label="이메일" v-model="email" color="#00d5aa"></v-text-field>
        <v-text-field
            v-model="password"
            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[ rules.required, rules.min]"
            :type="show1 ? 'text' : 'password'"
            name="input-10-1"
            label="비밀번호"
            counter
            color="#00d5aa"
            @click:append="show1 = !show1" @keyup.enter="login"
        ></v-text-field>
        <br>
        <v-btn class="btn-padding-0" rounded outlined color="grey" @click="login"> 로그인 </v-btn><br><br>
        <div id="loginPage">
            <a href="/signup" >회원가입</a><br>
            <a href="/forgotPassword">비밀번호 찾기</a>
        </div>
    </v-card-text>
</template>
<script>
import Vue from 'vue'
import { Auth } from 'aws-amplify';
import router from '../../router'
import {validateEmail} from '@/utils/validation'
import http from '../../http/http-common'

    export default Vue.extend({
        props: {
            info: Object
        },
		data: () => ({
            email: '',
            show1: false,
            show2: true,
            show3: false,
            show4: false,
            registerEmail: '',
            password: '',
            nickname: '',
            err: {},
            rules: {
            required: value => !!value || 'Required.',
            min: v => v.length >= 8 || 'Min 8 characters',
            emailMatch: () => (`The email and password you entered don't match`),

            }
		}),
		name: "LoginPage",
		components:{
		},
        created(){
            this.email = this.info.email
            this.nickname = this.info.nickname
        },
        methods: {
            reset(){
                this.email = '';
                this.password='';
                this.$refs.email.focus();
            },
            async getUserInfo(){
                await http
                    .get('/users/'+this.email,{
						// headers:{
						// 	'Authorization': 'Bearer '+localStorage.getItem('accessToken')
						// }
                    })
                    .then(response => {
                        this.$store.commit('setUserInfo', response.data);
                        localStorage.setItem('userInfo', JSON.stringify(response.data))
                        window.open("/","_self"); 
                    })
                    .catch(() => this.errored = true )
                    .finally(() => {
                        this.loading = false
                    })
            },
            async login(){
                if(validateEmail(this.email)==false){
                    alert("이메일 형식이 올바르지 않습니다.");
                    this.reset();
                    return;
                }else if(this.email == '' || this.password == ''){
                    alert("이메일과 비밀번호를 모두 입력해주세요.")
                    this.reset();
                    return;
                }
                try {
                    await Auth.signIn(this.email, this.password)
                            .then(user => {
                                this.$store.commit('changeSignedInState', user);
                                Auth.currentSession()
                                    .then(result => {
                                        this.$store.commit('setAccessToken', result.accessToken.jwtToken);
                                        localStorage.setItem('accessToken', this.$store.state.accessToken)
                                        this.getUserInfo()
                                    })
                            })
                            .catch(err => {
                                this.err = err
                                if(err.code === "NotAuthorizedException"){
                                        alert("이메일 혹은 비밀번호가 잘못되었습니다.");
                                        this.reset();
                                }else if(err.code === "UserNotFoundException"){
                                    alert("등록되지 않는 계정입니다.");
                                    this.reset();
                                }
                            })
                            .finally(() => {
                                console.log("finally") 
                            });

                } catch (error) {
                    console.log('error signing in', error);
                }
            }
        },
	})
</script>
<style>

#loginPage a:link {
  color: #757575 !important;
  background-color: transparent;
  text-decoration: none;
  text-decoration: underline;
}
#loginPage a:visited {
  color: #757575 !important;
  background-color: transparent;
  text-decoration: none;
}
#loginPage a:hover {
  color: #00d5aa !important;
  background-color: transparent;
  text-decoration: underline;
}
</style>