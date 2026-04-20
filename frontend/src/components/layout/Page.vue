<template>
  <div id="item">
        <v-flex v-for="article in articles" v-bind:key="article.id">
          <v-card
            class="mx-auto"
            max-width="55%"
            max-height="600"
            tile
          >
            <div class="card" @click="articlePage(article.id)">
              <v-card-text class="text newest-article">
                <h2 v-html="article.title"></h2><br>
                <!-- <h3 style="font-weight: normal" v-html="article.subtitle"></h3> -->
                <p v-html="article.contents ? article.contents : ''"></p>
              </v-card-text>

              <v-card-actions class="avatar-box">
                  <v-list-item-avatar class="page-avatar" color="grey darken-3" style="width: 15px; height: 15px;">
                    <v-img
                      class="avatar"
                      alt="avatar"
                      src="https://avataaars.io/?avatarStyle=Transparent&topType=ShortHairShortCurly&accessoriesType=Prescription02&hairColor=Black&facialHairType=Blank&clotheType=Hoodie&clotheColor=White&eyeType=Default&eyebrowType=DefaultNatural&mouthType=Default&skinColor=Light"
                    ></v-img>
                  </v-list-item-avatar>
                  <v-list-item-content class="author-date">
                    <span class="nickname" v-html="article.nickName"></span>
                    
                  </v-list-item-content>
                  <span class="right-padding">{{dateTime(article.modDatetime)}}</span>
              </v-card-actions>
              <br/>
            </div>
          </v-card>
          <br>
        </v-flex>
        
        <div class="text-center">
          <v-pagination v-model="page" :length="totalPageNum" :total-visible="7" prev-icon="mdi-menu-left" next-icon="mdi-menu-right" @input="changePage">
          </v-pagination>
        </div>
    
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import http from '../../http/http-common'

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
        async getArticles(pageNum: number){
          console.log('getArticles')
          await http
              .get('/board', {
                params: { 'pageNumber': pageNum },headers:{
                        'Authorization': 'Bearer '+localStorage.getItem('accessToken')
                    }})
              .then(response => {
                  console.log(response.data)
                  response.data.forEach((d: any) => {
                    if(d.contents.length != 0){
                      if(d.contents[0].content.length > 150){
                        d.contents = d.contents[0].content.substr(0,148)+"..."
                      }else{
                        d.contents = d.contents[0].content
                      }
                    }else{
                      d.contents = ""
                    }
                    
                  })
                  this.articles = response.data;
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
              .get('/board/count')
              .then(response => {
                      this.totalPageNum = Math.floor(response.data / 5) + 1
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
        console.log("mounted")
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
</style>