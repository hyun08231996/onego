<template>
  <div id="following-list" class="follow-list">
      <h1 class="follow-title">{{nickname}} 작가를 구독하는 작가 {{this.followeridList.length}}명</h1>
      <br><br>
      <v-flex v-for="follower in followerInfoList" v-bind:key="follower.email">
        <v-card
          class="mx-auto followbox-margin-top"
          max-width="55%"
          max-height="600"
          tile
        >
          <div class="card" @click="writerProfile(follower.email)">
            <v-card-actions class="avatar-box">
                <v-list-item-avatar class="page-avatar" color="grey darken-3" style="width: 15px; height: 15px;">
                  <v-img
                    class="avatar"
                    alt="avatar"
                    :src="follower.profileImage"
                  ></v-img>
                </v-list-item-avatar>
                <v-list-item-content class="author-date">
                  <span class="nickname" v-html="follower.nickName"></span>
                  <span class="right-padding modDatetime" v-html="follower.intro"></span>
                </v-list-item-content>
                <!-- unsubscribed button -->
                <v-btn class="button unsubscribe-btn" @click="unsubscribe($event, follower.email), follower.flag='false'" value="" rounded v-if="follower.flag=='true'">
                </v-btn>

                <!-- subscribe button -->
                <v-btn class="button subscribe-btn" @click="subscribe($event, follower.email), follower.flag='true'" rounded v-if="follower.flag=='false'">
                    구독하기
                </v-btn>
            </v-card-actions>
            <br/>
          </div>
        </v-card>
        <br>
      </v-flex>
  </div>
</template>

<script>
import Vue from 'vue'
import http from '../http/http-common'

export default Vue.extend({
    data: () => ({
            email: "",
            nickname: "",
            followeridList: [],
            followerInfoList: [],
            errored: false,
            loading: true
        }),
    name: 'FollowerList',
    methods: {
        writerProfile(writerEmail){
            this.$router.push({
                name: "MyProfile",
                params: { emailProp: writerEmail },
            });
        },
        async getUserInfo(userEmail){
            var userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
            await http
                    .get('/users/'+userEmail)
                    .then(response => {
                        if(userInfo.email == response.data.email){
                          response.data['flag']="me"
                        }else{
                          for(var i=0; i<userInfo.followings.length; i++){
                            if(userInfo.followings[i] == response.data.email){
                              response.data['flag']="true"
                              break
                            }else{
                              response.data['flag']="false"
                            }
                          }
                        }
                        this.followerInfoList.push(response.data)
                    })
                    .catch(() => this.errored = true )
                    .finally(() => {
                        this.loading = false
                    })  
        },
        async unsubscribe(e, email){
            var userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
            e.stopPropagation();
            await http
                .delete('/followings/'+this.$store.state.user.userAccount.attributes.email, {data: {'followEmail': email},
                  headers:{
                    'Authorization': 'Bearer '+localStorage.getItem('accessToken')
                  }})
                .then(response => {
                    userInfo.followings = userInfo.followings.filter((element) => element !== email)
                    localStorage.setItem('userInfo', JSON.stringify(userInfo))
                })
                .catch(() => this.errored = true )
                .finally(() => {
                    this.loading = false
                })
        },
        async subscribe(e, email){
            var userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
            e.stopPropagation();
            await http
                .post('/followings/'+this.$store.state.user.userAccount.attributes.email, {'followEmail': email},{
                  headers:{
                    'Authorization': 'Bearer '+localStorage.getItem('accessToken')
                  }})
                .then(response => {
                    userInfo.followings.push(email)
                    localStorage.setItem('userInfo', JSON.stringify(userInfo))
                })
                .catch(() => this.errored = true )
                .finally(() => {
                    this.loading = false
                })
        }
    },
    async mounted() {
        this.email = this.$store.state.followerUser
        if(this.email == this.$store.state.user.userAccount.attributes.email){
            await http
              .get('/users/'+this.email)
              .then(response => {
                  this.$store.commit('setUserInfo', response.data);
                  this.nickname = this.$store.state.user.userInfo.nickName;
                  this.followeridList = this.$store.state.user.userInfo.followers;
              })
        }else{
            await http
              .get('/users/'+this.email,)
              .then(response => {
                  this.nickname = response.data.nickName
                  this.followeridList = response.data.followers;
              })
        }  
        
        for(var i=0; i<this.followeridList.length; i++){
            this.getUserInfo(this.followeridList[i])
        }
    }
})

</script>

<style>
  .follow-title{
      text-align: center;
      font-weight: 400;
  }
  .followbox-margin-top{
      padding-top: 20px;
      
  }
  .follow-list{
      font-family: "Noto Sans KR", sans-serif !important;
  }
  .unsubscribe-btn{
      background-color: #00d5aa !important;
      color: white !important;
  }
  .unsubscribe-btn::after{
    content: "구독중 ✓";
    -webkit-box-shadow: none;
    -moz-box-shadow: none;
    box-shadow: none;
  }
  .unsubscribe-btn:before {
    transition-duration: 0.4s;
  }

  .unsubscribe-btn:hover{
    background-color: white !important; 
    color: #00d5aa !important;
    
  }
  .unsubscribe-btn:hover:after{
    content: "구독해지" !important;
    -webkit-box-shadow: none;
    -moz-box-shadow: none;
    box-shadow: none;
  }

  .subscribe-btn{
    /* border: 0.1px solid #00d5aa; */
    background-color: white !important;
    color: #00d5aa !important;
  }
  
</style>