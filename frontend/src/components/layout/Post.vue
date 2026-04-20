<template>
  <div class="post">
    
        <!-- Title Image -->
        <v-card v-if="article.titleImage !== null && article.titleImage !== ''" tile class="mb-12" id="post-image-card">
            <v-img height="50vh" :src="article.titleImage">
              <v-flex id="post-title-preview-margin">
              <span><h1 style="font-size:40px; padding-left:1px; max-width:80%;" v-html="article.title"></h1></span>  
              <div style="opacity:80%;"><h3 v-html="article.subtitle"></h3></div>
              <div style="opacity:60%;margin-top:30px;">
                <span><h5> {{ article.nickName }} · {{getTime(article.modDatetime)}} </h5></span>
              </div>
              </v-flex>
            </v-img>
        </v-card>
      <!--Title content-->
      <v-flex v-if="article.titleImage == null || article.titleImage == ''" id="post-title-content-preview-margin" class="mx-auto mb-16">
        <h1 style="font-size:40px;" v-html="article.title"></h1>
        <div style="opacity:80%;"><h3 v-html="article.subtitle"></h3></div>
        <div style="opacity:60%;margin-top:30px;"><h5> {{ article.nickName }} · {{getTime(article.modDatetime)}} </h5></div>
      </v-flex>
        
      <!-- Content -->
      <v-flex id="post-content-preview-margin" class="mx-auto">
          <div v-for="(content,i) in article.contents" :key="i">
            <h3 v-html="content.subtitle"></h3>
            <p style="padding-top: 10px; padding-bottom: 30px; line-height:30px;" v-html="content.content"></p>
          </div>
      </v-flex>

      <!-- Tags -->
      <v-flex id="post-tag-preview-margin" class="mx-auto mt-8 pb-8">
        <span  v-for="tag in article.tags" :key="tag">
          <v-chip outlined small color="#00d5aa" class="mr-2">{{ tag }}</v-chip>
        </span>
      </v-flex>

      <!-- <div style="height: 60px;"></div> -->
      <Comment :boardId = "article.id"/>   
      
      <!-- <div style="height: 60px;"></div> -->
      <Profile :id = "article.userEmail"/>
   
  </div>
</template>


<script lang="ts">
import Vue from 'vue';
import Profile from '@/components/layout/Profile.vue'
import Comment from '@/components/layout/Comment.vue'
import http from '../../http/http-common'

export default Vue.extend({

    data: () => ({
          errored: false,
          loading: true,
          content: '',
          page: 1,
          article : {},
          user: {},
          titleImageFile: new File([""], ""),
          id : '',
          userId : '',
          loginUser:'',
          scraps:false
    }),
    components:{
       Comment, Profile
    },
    methods: {
        getTime(time: any){
            const temp = new Date(time)
            const date = temp.getFullYear()+". "+temp.getMonth()+". "+temp.getDate()
            return date
        },
        async getArticle(boardId: string){
          var userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
          await http
              .get('/board', {
                params: { 'boardId': boardId }, 
                })
              .then(response => {
                  this.article = response.data[0];
                  //console.log(response.data[0].titleImage)
                  if(this.loginUser != undefined){
                    for(var i=0; i<userInfo.likes.length; i++){
                        if(boardId === userInfo.likes[i]){
                            this.scraps = true
                            break
                        }
                    }
                  }
              })
        }
          
    },
    created(){  
      var userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')
      this.loginUser = userInfo.email
      this.getArticle(this.$route.params.boardId)
    }
})
</script>


<style >
  /* .mx-auto justify-center{
    margin: 0 auto;
  } */
	.post {
		font-family: "Noto Sans KR", sans-serif !important;
	}
  .postbtn{
    vertical-align: middle;
    float: right;
    padding-left: 10px;
    padding-top: 9.5px;
  }
  #post-image-card{
    margin-top:-36px !important;
    position:relative !important;
  }
  .likescount{
    padding-top: 5px;
    color: #00d5aa;
    font-size: 1.1rem;
  }
  #post-title-preview-margin{
    width:50% !important;
    position:absolute !important;
    bottom:10% !important;
    left:25% !important;
  }

  #post-image-card .v-image__image{
    opacity:0.7 !important;
  }

  #post-title-content-preview-margin,
  #post-content-preview-margin,
  #post-tag-preview-margin{
    max-width:50% !important;
  }
</style>