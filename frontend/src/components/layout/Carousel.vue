<template>
  <div id="carousel">
    <v-slide-group
      
      class="pa-4"
      active-class="success"
      show-arrows
    >
    <!-- v-model="model" -->
      <v-slide-item
        v-for="article in articles"
        :key="article.id"
        v-slot="{ active }"
      >
      
        <v-card
          :color="active ? undefined : 'grey lighten-1'"
          class="ma-0"
          height="550"
          width="700"
          style="padding: 1px"
          @click="articlePage(article.id)"
        >
        
          <v-row
            class="fill-height"
            align="center"
            justify="center"
          >
            <v-img id="carouselImg" :src="article.titleImage"></v-img>
            <div id="articleTitle">{{article.title}}</div>
            <div id="articleAuthor">by. {{article.nickName}}</div>
          </v-row>
        </v-card>
      </v-slide-item>
    </v-slide-group>
  </div>
</template>
<script>
  import http from '../../http/http-common'
  export default {
    data: () => ({
      articles: []
		}),
		name: "Carousel",
		components:{
		},
        methods: {
            async getArticles(idx){
                await http
                    .get('/board', {
                        params: { 'pageNumber': idx }})
                    .then(response => {
                        response.data.forEach((d) => {
                          if(d.titleImage != null){
                            if(d.titleImage.length != 0){
                              this.articles.push(d)
                            }
                          }
                        })
                        // 최신순으로 정렬
                        this.articles = this.articles.sort((a, b) => new Date(b.modDatetime) - new Date(a.modDatetime))
                    })
            },
            articlePage(boardId){
              window.open("/content/"+boardId,"_self");
            }
        },
        mounted() {
            var i = 1
            for(i; i<10; i++){
              this.getArticles(i)
              if(this.articles.length > 6)
                break;
            }
        }
  }
</script>
<style>

    #carouselImg {
      background: #CCC;
      filter: alpha(opacity=60);
      /* IE */
      -moz-opacity: 0.8;
      /* Mozilla */
      opacity: 0.8;
      /* CSS3 */
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      width: 100%;
    }
    #articleTitle {
      color: white;
      position: absolute;
      text-align: center !important;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      font-size: 50px;
      font-weight: 500;
      top: 50%;
    }
    #articleAuthor {
      color: white;
      position: absolute;
      text-align: center !important;
      width: 100%;
      height: 100%;
      font-size: 15px;
      font-weight: 500;
      top: 80%;
    }
</style>