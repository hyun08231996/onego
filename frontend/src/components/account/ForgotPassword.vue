<template>
    <v-card-text>
        <p class="text-h4 text--primary">비밀번호 찾기</p><br>
        <v-text-field ref="resetEmail" color="#00d5aa" label="이메일" v-model="resetEmail" @keyup.enter="getConfirmationCode"></v-text-field><br>
        <v-btn class="btn-padding-0" rounded outlined color="grey" @click="getConfirmationCode"> 인증번호 받기 </v-btn><br>
    </v-card-text>
</template>
<script>
import Vue from 'vue'
import { Auth } from 'aws-amplify'
    
    export default Vue.extend({
        name: 'SignUp',
        props: {
            email: String
        },
        data: () => ({
            resetEmail: '',
        }),
        created(){
            // this.resetEmail = this.email
        },
        methods: {
            async getConfirmationCode(){
                Auth.forgotPassword(this.resetEmail)
                    .then(data => {
                        this.$set(this.$parent.$parent.$data, 'email', this.resetEmail)
                        })
                    .catch(err => console.log(err));
            },
        }
    })
</script>