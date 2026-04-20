<template>
    <div>
        <v-flex id="setting-margin" class="mx-auto">
            <div align="center" class="spacing">
                <h2 id="title">계정설정</h2>
            </div>
            <div class="spacing">
                <label class="subtitle"><strong>계정</strong></label>
                <div class="center-space">
                    <span class="content" style="font-size:1em;">{{user.email}}</span>
                    <span class="button"><v-btn id="change-btn"
                        rounded
                        outlined
                        color="grey"
                        href="/change-pass">
                        비밀번호 변경</v-btn>
                    </span>
                </div>
            </div>
            <v-divider class="divider"/>
            <div class="spacing">
                <label class="subtitle"><strong>프로필</strong></label>
                <div class="center-space">
                    <span class="content">
                        <div class="content-info"><label style="font-size:1.2em;">{{user.nickname}}</label></div>
                        <div class="content-info"><label style="font-size:0.9em;opacity:75%;">{{user.intro}}</label></div>
                    </span>
                    <span class="button" id="pic-btn">
                        <v-list-item-avatar size=90>
                            <img :src="user.pic">
                        </v-list-item-avatar><br>
                        <v-btn id="edit-btn"
                            rounded
                            outlined
                            color="rgb(0, 213, 170)"
                            @click="editProfile">
                            프로필 수정
                        </v-btn>
                    </span>
                </div>
            </div>
            <v-divider class="divider"/>
        </v-flex>
    </div>

</template>

<script lang="ts">
    import Vue from 'vue'
    import http from '../http/http-common'
    import { Auth } from 'aws-amplify'
    
    export default Vue.extend({
        name:"Setting",
        data: () => ({
            user:{
                nickname:'Mary',
                email:'mj123@gmail.com',
                intro:'Hello, I am an avid writer',
                pic:"https://randomuser.me/api/portraits/women/82.jpg"
            },
        }),
        methods:{
            editProfile(){
                location.href="/edit-prof";
            }
        },
        async mounted(){
            var userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
            this.user.nickname = this.$store.state.user.userAccount.attributes.nickname
            this.user.email = this.$store.state.user.userAccount.attributes.email
            this.user.intro = userInfo.intro
            this.user.pic = userInfo.profileImage
        }
    })
</script>

<style>
#setting-margin{
    max-width:55%;
    margin-top: -25px;
}
.spacing{
    margin-bottom:30px;
}
.divider{
    margin-top:30px;
    margin-bottom:30px;
}
#title{
    color:grey;
}
.subtitle{
    font-weight:bold;
    font-size:0.75em;
}
.content{
    margin-top:10px;
    margin-left:5px;
    color:#505050;
}
.center-space{
    margin-top:10px;
    display: flex;
}
.content{
    flex: 1;
}
#pic-btn{
    margin-right: -8px !important;
    margin-top: -70px;
}
.content-info{
    margin-bottom:10px;
}
#change-btn:hover{
    color:#757575 !important;
}
#edit-btn:hover{
    color:#02bf99 !important;
}
</style>