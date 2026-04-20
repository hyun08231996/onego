<template>
  <div id="following-list" class="follow-list">
      <h1 class="follow-title">{{nickname}} 작가가 구독하는 작가 {{this.followidList.length}}명</h1>
      <br><br>
      <v-flex v-for="following in followInfoList" v-bind:key="following.email">
        <v-card
          class="mx-auto followbox-margin-top"
          max-width="55%"
          max-height="600"
          tile
        >
          <div class="card" @click="writerProfile(following.email)">
            <v-card-actions class="avatar-box">
                <v-list-item-avatar class="page-avatar" color="grey darken-3" style="width: 15px; height: 15px;">
                  <v-img
                    class="avatar"
                    alt="avatar"
                    :src="following.profileImage"
                  ></v-img>
                </v-list-item-avatar>
                <v-list-item-content class="author-date">
                  <span class="nickname" v-html="following.nickName"></span>
                  <span class="right-padding modDatetime" v-html="following.intro"></span>
                </v-list-item-content>
                <!-- unsubscribed button -->
                <v-btn class="button unsubscribe-btn" @click="unsubscribe($event, following.email), following.flag='false'" value="" rounded v-if="following.flag=='true'">
                </v-btn>

                <!-- subscribe button -->
                <v-btn class="button subscribe-btn" @click="subscribe($event, following.email), following.flag='true'" rounded v-if="following.flag=='false'">
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
            followidList: [],
            followInfoList: [],
            errored: false,
            loading: true
        }),
    name: 'FollowingList',
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
                        if(this.$store.state.user.userAccount.attributes.email == userEmail){
                          response.data['flag']="me"
                        }else{
                          for(var i=0; i<userInfo.followings.length; i++){
                            if(userInfo.followings[i] == userEmail){
                              response.data['flag']="true"
                              break
                            }else{
                              response.data['flag']="false"
                            }
                          }
                        }
                        this.followInfoList.push(response.data)
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
                    //update local storage
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
                    //update local storage
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
        this.email = this.$store.state.followingUser
        if(this.email == this.$store.state.user.userAccount.attributes.email){
          var userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
          this.nickname = userInfo.nickName;
          this.followidList = userInfo.followings;
        }else{
            await http
              .get('/users/'+this.email)
              .then(response => {
                  this.nickname = response.data.nickName
                  this.followidList = response.data.followings;
              })
        }  
        
        for(var i=0; i<this.followidList.length; i++){
            this.getUserInfo(this.followidList[i])
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