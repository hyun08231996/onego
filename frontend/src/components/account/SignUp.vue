<template>
    <v-card-text>
        <p class="text-h4 text--primary">SIGN UP</p><br>
        <!-- <p v-if="errors.length">
            <b>아래 오류를 수정하세요.:</b>
            <ul>
            <li v-for="error in errors">{{ error }}</li>
            </ul>
        </p> -->
        <v-text-field ref="registerEmail" label="이메일" v-model="registerEmail" color="#00d5aa"></v-text-field>
        <v-text-field label="닉네임" v-model="nickname" color="#00d5aa"></v-text-field>
        <v-text-field
            v-model="password"
            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'" 
            :rules="[rules.required, rules.min]"
            :type="show1 ? 'text' : 'password'"
            name="input-10-1"
            label="비밀번호"
            hint="At least 8 characters"
            counter
            color="#00d5aa"
            @click:append="show1 = !show1"
            @keyup.enter="signUpCheck"
        ></v-text-field><br>
        <v-btn class="btn-padding-0" rounded outlined color="grey" @click="signUpCheck"> 회원가입 </v-btn><br>
    </v-card-text>
</template>
<script>
import Vue from 'vue'
import { Auth } from 'aws-amplify'
import {validateEmail} from '@/utils/validation'
import http from '../../http/http-common'
    
    export default Vue.extend({
        name: 'SignUp',
        props: {
            info: Object
        },
        data: () => ({
            show1: false,
            show2: true,
            show3: false,
            show4: false,
            registerEmail: '',
            password: '',
            nickname: '',
            rules: {
            required: value => !!value || 'Required.',
            min: v => v.length >= 8 || 'Min 8 characters',
            emailMatch: () => (`The email and password you entered don't match`),
            
            }
        }),
        created(){
            this.registerEmail = this.info.email;
            this.nickname = this.info.nickname;
        },
        methods: {
            reset(){
                this.registerEmail = '';
                this.password ='';
                this.nickname ='';
                this.$refs.registerEmail.focus();
            },
            async postUser(email, nickName){
                await http
                    .post('/users', {'email': email, 'nickName': nickName })
                    .then(response => {
                        console.log(response)
                    })
            },
            signUpCheck(){
                if(this.registerEmail=='' || this.nickname=='' || this.password ==''){
                    alert("이메일, 닉네임, 그리고 비밀번호를 모두 입력해주세요.");
                    this.reset();
                    return;
                }else if(validateEmail(this.registerEmail)==false){
                    alert("이메일 형식이 올바르지 않습니다.")
                    this.reset();
                    return;
                }else if(this.password.length < 8){
                    alert("8자리 이상의 비밀번호를 입력해주세요.")
                    this.reset();
                    return;
                }
                try {
                    Auth.signUp({
                        username: this.registerEmail,
                        password: this.password,
                        attributes: {          // optional - E.164 number convention
                            email: this.registerEmail,
                            nickname: this.nickname,// other custom attributes 
                        }
                    })
                    .then(user =>{
                        this.$set(this.$parent.$parent.$data.info, 'email', this.registerEmail)
                        this.$set(this.$parent.$parent.$data.info, 'nickname', this.nickname)
                        this.postUser(this.registerEmail, this.nickname)
                    })
                    .catch(err => {
                        if(err.code === "UsernameExistsException"){
                            this.reset();
                            alert("이미 등록된 이메일입니다. 다른 이메일을 입력해주세요.");   
                        }
                    });
                    
                } catch (error) {
                    console.log('error signing up:', error);
                }
            }
        }
    })
</script>