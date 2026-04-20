<template>
  <div id="scrap">
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

            <v-card-actions class="avatar-box"  @click="writerProfile($event, article.userEmail)">
                <v-list-item-avatar class="page-avatar" color="grey darken-3" style="width: 15px; height: 15px;">
                  <v-img
                    class="avatar"
                    alt="avatar"
                    :src="article.titleImage"
                  ></v-img>
                </v-list-item-avatar>
                <v-list-item-content class="author-date">
                  <span class="nickname" v-html="article.nickName"></span>
                </v-list-item-content>
                <span class="right-padding modDatetime">{{getTime(article.modDatetime)}}</span>
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
        articles: [],
        errored: false,
        loading: true,
        content: '',
        page: 1,
        totalPageNum: 1,
        scrapId: {},
		  }),
      methods: {
        writerProfile(e, writerEmail){
            e.stopPropagation()
            this.$router.push({
                name: "MyProfile",
                params: { emailProp: writerEmail },
            });
        },
        getContents(boardId){
          http
            .get('/board', {
                params: { 'boardId': boardId }},{
                headers:{
                  'Authorization': 'Bearer '+localStorage.getItem('accessToken')
                }})
              .then(response => {
                http 
                  .get('/users/'+response.data[0].userEmail)
                  .then(r => {
                      response.data[0].nickName = r.data.nickName
                      if(r.data.profileImage != undefined){
                        response.data[0].titleImage = r.data.profileImage
                      }else{
                        response.data[0].titleImage = ''
                      }
                  })
                if(response.data.length !=0){
                  response.data.forEach((d) => {
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
                  this.articles.push(response.data[0])
                }
              })
        },
        async getScrapId(){
          var userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
          this.scrapId = userInfo.likes
          for(let i = 0; i< this.scrapId.length; i++){
              this.getContents(this.scrapId[i])
          }
        },
        getTime(time){
            const temp = new Date(time)
            const date = temp.getFullYear()+". "+temp.getMonth()+". "+temp.getDate()
            return date
        },
        articlePage(boardId){
          window.open("/content/"+boardId,"_self");
        },

      },
      created(){
        this.getScrapId()
        
      }
    })

</script>

<style>
  .right-padding{
    padding-right: 30px
  }
  #scrap {
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