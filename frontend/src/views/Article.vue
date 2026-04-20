<template>
  <div id="textArea">
    <div id="item">
       <v-flex v-for="article in articles" v-bind:key="article.id">
         <v-card
           class="mx-auto"
           max-width="55%"
           max-height="600"
           tile
         >  
           <div id="content-hover" class="card" @click="articlePage(article.id)">
             <v-img
               v-if="article.titleImage"
               :src="article.titleImage"
               height="200"
               class="article-cover"
             />
             <v-card-text class="text newest-article">
               <h2 id="content-title" v-html="article.title"></h2><br>
               <!-- <h3 style="font-weight: normal" v-html="article.subtitle"></h3> -->
               <p v-html="article.contents ? article.contents : ''"></p>
             </v-card-text>

             <v-card-actions class="avatar-box" @click="writerProfile($event, article.userEmail)">
                <!-- <div id="userProfile" @click="writerProfile($event, article.email)"> -->
                  <v-list-item-avatar class="page-avatar" color="grey darken-3" style="width: 15px; height: 15px;">
                    <v-img
                      class="avatar"
                      alt="avatar"
                      :src="article.profileImage"
                    ></v-img>
                  </v-list-item-avatar>
                  <v-list-item-content class="author-date">
                    <span class="nickname" v-html="article.nickName"></span>
                  </v-list-item-content>
                 <!-- </div> -->
                 <span class="right-padding">{{dateTime(article.modDatetime)}}</span>
             </v-card-actions>
           </div>
         </v-card>
         <br>
       </v-flex>

       <div class="text-center">
         <v-pagination v-model="page" :length="totalPageNum" :total-visible="7" prev-icon="mdi-menu-left" next-icon="mdi-menu-right" @input="changePage">
         </v-pagination>
       </div>
      </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import http from '../http/http-common'
import { eventBus } from '@/main'

export default Vue.extend({
     data: () => ({
      articles: {},
      errored: false,
      loading: true,
      content: '',
      page: 1,
      totalPageNum: 1
     }),
     methods: {
       writerProfile(e: any, writerEmail: string){
            e.stopPropagation()
            this.$router.push({
                name: "MyProfile",
                params: { emailProp: writerEmail },
            });
        },
       async getArticles(pageNum: number){
         await http
             .get('/board', {
               params: { 'pageNumber': pageNum }})
             .then(async response => {
                const enrichedArticles = await Promise.all(
                  response.data.map(async (d: any) => {
                    let nickName = d.nickName;
                    let profileImage = '';

                    try {
                      const userResponse = await http.get('/users/' + d.userEmail);
                      nickName = userResponse.data.nickName;
                      profileImage = userResponse.data.profileImage || '';
                    } catch (error) {
                      profileImage = '';
                    }

                    let previewContent = "";
                    if (d.contents.length !== 0) {
                      const primaryContent =
                        d.contents[0].content.length !== 0
                          ? d.contents[0].content
                          : (d.contents[1]?.content || "");

                      previewContent =
                        primaryContent.length > 100
                          ? primaryContent.substr(0, 97) + "..."
                          : primaryContent;
                    }

                    return {
                      ...d,
                      nickName,
                      profileImage,
                      contents: previewContent,
                    };
                  })
                );

                this.articles = enrichedArticles;
             })
             .catch(() => {
               this.errored = true
             })
             .finally(() => this.loading = false)

           },
       difference(date1: { getFullYear: () => number; getMonth: () => number; getDate: () => number|undefined; getHours: () => number|undefined; getMinutes: () => number|undefined; getSeconds: () => number|undefined }, date2: { getFullYear: () => number; getMonth: () => number; getDate: () => number|undefined; getHours: () => number|undefined; getMinutes: () => number|undefined; getSeconds: () => number|undefined }) {
         const date1utc = Date.UTC(date1.getFullYear(), date1.getMonth(), date1.getDate(), date1.getHours(), date1.getMinutes(), date1.getSeconds());
         const date2utc = Date.UTC(date2.getFullYear(), date2.getMonth(), date2.getDate(), date2.getHours(), date2.getMinutes(), date2.getSeconds());
         const day = 1000*60*60*24;
         const hour = 1000*60*60;
         const minute = 1000*60;
         const second = 1000;
         if((date2utc - date1utc)/day > 1){
           return Math.floor((date2utc - date1utc)/day)+"일 전"
         }else if((date2utc - date1utc)/hour > 1){
           return Math.floor((date2utc - date1utc)/hour)+"시간 전"
         }else if((date2utc - date1utc)/minute > 1){
           return Math.floor((date2utc - date1utc)/minute)+"분 전"
         }else{
           return Math.floor((date2utc - date1utc)/second)+"초 전"
         }

       },
       dateTime(time: string|number|Date) {
         const articleDate =  new Date(time)
         const current = new Date();
         return this.difference(articleDate, current)
       },
       changePage(value: number){
         this.page = value
         this.getArticles(this.page)
       },
       async boardCount(){
         await http
             .get('/board/count',{
				//  headers:{
				// 	'Authorization': 'Bearer '+localStorage.getItem('accessToken')
				//  }
			 })
             .then(response => {
                    if(response.data%5==0){
                      this.totalPageNum = Math.floor(response.data / 5)
                    }else{
                      this.totalPageNum = Math.floor(response.data / 5) + 1
                    }
                   }
                 )
             .catch(() => this.errored = true )
             .finally(() => this.loading = false)
       },
       articlePage(boardId: string){
         window.open("/content/"+boardId,"_self");
       }

     },
     async created(){
       this.getArticles(1)
       this.boardCount()
     }
     
   })

</script>
<style>
  #item {
   font-family: "Noto Sans KR", sans-serif !important;
 }
 .card{
    padding: 15px;
 }
 .article-cover{
    border-bottom: 1px solid rgba(0, 0, 0, 0.06);
 }
 .text{
   padding-top: 30px;
   padding-bottom: 5px;
 }
 .text-post{
   font-size : 1.1rem;
   line-height: 1.7em;
   font-weight: 300;
   letter-spacing: 0;
   /* 글자수 제한*/
   overflow: hidden;
   text-overflow: ellipsis;
   display: -webkit-box;
   -webkit-line-clamp: 3;
   -webkit-box-orient: vertical;
   word-wrap:break-word;
   height: 5.1em; /*height는 1.7em * 3줄 = 5.1em */
 }
 .avatar-box{
   padding-left: 17px;
 }
 .newest-article{
   padding-bottom: 0px !important;
 }
 .page-avatar{
   margin-top: 5px;
   margin-bottom: 0px;
   height: 50px !important;
   min-width: 50px !important;
   width: 50px !important;
 }
 #content-hover:hover{
   cursor: pointer;
 }
 #content-hover:hover #content-title{
   color:#00d5aa;
 }
</style>
