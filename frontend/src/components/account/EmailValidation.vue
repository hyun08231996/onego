<template>
    <v-card-text>
        <p class="text-h4 text--primary">Email 확인</p><br>
        <p class="text--primary">입력하신 이메일로 전송된 메일을 확인해주세요.</p>
        <v-text-field v-model="registerEmail"  v-if="this.email == ''" disabled></v-text-field>
        <v-text-field v-model="resetEmail"  v-if="this.email != ''" disabled></v-text-field>
        <v-text-field label="확인코드" v-model="validationCode" @keyup.enter="validateEmail" v-if="this.email == ''" color="#00d5aa"></v-text-field>
        <v-text-field label="확인코드" v-model="validationCode" @keyup.enter="validateEmail" v-if="this.email != ''" color="#00d5aa"></v-text-field>
        <v-text-field
            v-model="newPassword"
            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'" 
            :rules="[rules.required, rules.min]"
            :type="show1 ? 'text' : 'password'"
            name="input-10-1"
            label="새로운 비밀번호"
            hint="At least 8 characters"
            counter
            color="#00d5aa"
            v-if="this.email != ''"
            @click:append="show1 = !show1"
            @keyup.enter="validateForgotPassword"
        ></v-text-field><br>
        <v-btn class="btn-padding-0" rounded outlined color="grey" @click="validateEmail" v-if="this.email == ''"> 확인 </v-btn><br>
        <v-btn class="btn-padding-0" rounded outlined color="grey" @click="validateForgotPassword"  v-if="this.email != ''"> 비밀번호 리셋 확인 </v-btn><br>
    </v-card-text>
</template>
<script>
import Vue from 'vue'
import { Auth } from 'aws-amplify';
import { eventBus } from '../../main'
import router from '../../router'

    export default Vue.extend({
        name: 'SignUp',
        props: {
            info: Object,
            email: String
        },
        data: () => ({
            show1: false,
            show2: true,
            show3: false,
            show4: false,
            validationCode: '',
            registerEmail: '',
            nickname: '',
            restEmail: '',
            newPassword: '',
            rules: {
                required: value => !!value || 'Required.',
                min: v => v.length >= 8 || 'Min 8 characters',
                emailMatch: () => (`The email and password you entered don't match`),
            }
        }),
        created(){
            this.registerEmail = this.info.email;
            this.nickname = this.info.nickname;
            this.resetEmail = this.email
        },
        methods: {
            confirmSignUp(username, code, nickname) {
                try {
                    Auth.confirmSignUp(username, code)
                    .then(user => {
                        router.push({ name: 'login', params: { email: username, nickname: nickname }})
                        }
                    )
                    .catch(err => {
                        console.log(err)
                        console.log(err.code)
                        if(err.code === "CodeMismatchException"){
                            this.validationCode ='';
                            alert("잘못된 코드입니다. 다시 입력해주세요");   
                        }
                    })
                } catch (error) {
                    console.log('error confirming sign up', error)
                }
            },
            validateEmail(){
                this.registerEmail;
                this.confirmSignUp(this.registerEmail, this.validationCode, this.nickname);
            },
            validateForgotPassword(){
                Auth.forgotPasswordSubmit(this.resetEmail, this.validationCode, this.newPassword)
                    .then(response => {
                        console.log(response)
                        alert("비밀번호 변경을 완료했습니다.")
                        router.push({ name: 'login'})
                    })
                    .catch(err => console.log(err));
            }
        }
    })
</script>