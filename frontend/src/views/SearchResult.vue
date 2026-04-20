<template>
  <div id="item">
	<v-card elevation="0">
	  <v-flex id="search-bar-container" class="mx-auto justify-center">
		<!-- search bar -->
		<v-text-field id="text-field" class="text_field"
			:value="search"
			color="#00d5aa"
			height="30px"
			single-line
			flat solo
			autofocus
			@keyup.enter="doSearch"
			>
		</v-text-field>
	  </v-flex>
	<!-- search result -->
	</v-card>
	<v-divider style="margin-bottom:50px;"></v-divider>
	<div v-if="filteredSearch.length===0">
	<v-flex>
		<v-card
			class="mx-auto"
			max-width="55%"
			max-height="600"
		>
			<v-card-text>검색 결과가 없습니다.</v-card-text>
		</v-card>
	</v-flex>
	</div>
	<div v-else>
	<v-flex>

      <v-card
        class="mx-auto"
        max-width="55%"
        max-height="600"
		tile
		elevation="3"
		:key="i" v-for="(article, i) in filteredSearch"
      >
	  	<a id="list-item" @click="openArticle(article.id)">
        <div class="card">
          <v-card-text class="text" >
            <div id="article-title" v-html="highlightTitle(article.title)">{{article.title}}</div>
            <br/>
            <div id="article-content" class="text-post" v-html="highlightTitle(article.content)">{{article.content}}</div>
          </v-card-text>

          <v-card-actions class="avatar-box">
              <v-list-item-avatar color="grey darken-3">
                <v-img
                  class="avatar"
                  alt="avatar"
                  :src="article.profileImage"
                ></v-img>
              </v-list-item-avatar>
              <v-list-item-content class="author-date">
                <span class="author">{{article.nickname}}</span>
                <span class="date">{{article.date}}</span>
              </v-list-item-content>
          </v-card-actions>
          <br/>
        </div>
		</a>
      </v-card>

    </v-flex>
	</div>
  </div>
</template>

<script lang="ts">
	import Vue from 'vue'
	import '@/assets/css/SearchResult.css'
	import http from '@/http/http-common'

	declare interface BlogList {
		id:string,
		nickname:string,
		title:string,
		allText:string,
		content:string,
		date:string,
		profileImage:string
	}

	export default Vue.extend({
		name:"SearchResult",
		props:{
			search : {
				type:String, required:true
			}
		},
		data: ()=>({
			errored:false,
			loading:true,
			totalPageNum:1,
			blogList:[] as BlogList[],
			newSearch:''
		}),
		components:{
		},
		methods:{
			doSearch(){
				this.newSearch = (document.getElementById('text-field') as HTMLTextAreaElement).value;
				if(this.newSearch == ""){
					alert("검색어를 입력해주세요.");
					return;
				}
				location.href = "/search/"+this.newSearch;
			},
			highlightTitle(title:string){
				const searchWord1 = this.search.replace(/\s/g, "").split("").join('|');
				const searchWord2 = this.search.split(" ").join('|');
				return title.replace(new RegExp(searchWord1, "gi"), match => {
					return '<span class="highlight">' + match + '</span>';
				}) && title.replace(new RegExp(searchWord2, "gi"), match => {
					return '<span class="highlight">' + match + '</span>';
				});
			},
			hightlightText(text:string){
				const searchWord1 = this.search.replace(/\s/g, "").split("").join('|');
				const searchWord2 = this.search.split(" ").join('|');
				return text.replace(new RegExp(searchWord1, "gi"), match => {
					return '<span class="highlight">' + match + '</span>';
				}) && text.replace(new RegExp(searchWord2, "gi"), match => {
					return '<span class="highlight">' + match + '</span>';
				});
			},
			async getBoardCount(){
				await http.
					get('/board/count',
					{
						headers:{
							'Authorization': 'Bearer '+localStorage.getItem('accessToken')
						}
					})
					.then(response => {
					   //console.log("ok")
                       this.totalPageNum = Math.ceil(response.data / 5)
					   //console.log(this.totalPageNum)
					})
					.catch(() => this.errored = true )
					.finally(() => this.loading = false)
				for(var i=1;i<=this.totalPageNum;i++){
					this.getAllBoards(i)
				}
			},
			async getAllBoards(pageNum:number){
			  await http.
				get('/board',{
					params:{
						'pageNumber':pageNum
					},
					// headers:{
					// 	'Authorization': 'Bearer '+localStorage.getItem('accessToken')
					// }
				})
				.then(response => {
					//console.log(pageNum)
					for(let i=0; i<response.data.length;i++){
						//console.log(response.data[i])
						const id = response.data[i].id
						//const nickname = response.data[i].nickName
						const title = response.data[i].title
						let content:string
						if(response.data[i].contents[0].content === ''){
							content = response.data[i].contents[1].content
							console.log(content)
						}else{
							content = response.data[i].contents[0].content
						}
						//const content = response.data[i].contents[0].content
						let allText:string
						allText = response.data[i].subtitle
						for(let j=0;j<response.data[i].contents.length;j++){
							allText += response.data[i].contents[j].title+response.data[i].contents[j].subtitle+response.data[i].contents[j].content
						}
						const dateTime = new Date(response.data[i].modDatetime)
						var mm = dateTime.getMonth() + 1 // getMonth() is zero-based
						var dd = dateTime.getDate()
						const date = [dateTime.getFullYear(),
										(mm>9 ? '' : '0') + mm,
										(dd>9 ? '' : '0') + dd
										].join('.')
						//console.log(id,nickname,title,content,allText,date)
						//console.log(i,title)
						let profileImage:string
							http.
								get('/users/'+response.data[i].userEmail,{
									headers:{
										'Authorization': 'Bearer '+localStorage.getItem('accessToken')
									}
								})
								.then(response => {
									//console.log(response.data.profileImage)
									if(response.data.profileImage != undefined){
										profileImage = response.data.profileImage
									}
									this.blogList.push({id:id,nickname:response.data.nickName,title:title,allText:allText,content:content,date:date,profileImage:profileImage})
								})
						
						console.log(this.blogList)
						//this.blogList.push({id:id,title:title,allText:allText})

					}
				})
				.catch(() => this.errored = true )
				.finally(() => {
					this.loading = false
				})
			},
			openArticle(boardId:string){
				window.open('/content/'+boardId,'_self')
			}
		},
		computed:{
			filteredSearch(){
				let matches : RegExpMatchArray | null;
				const searchArray : string[] = this.search.split(" ");
				var str1 = "(?=.*";
				var str2 = ")";
				var searchStr = '';
				return this.blogList.filter((blog)=>{
					if(this.search != ""){
						//console.log(this.search);
						//console.log(blog.title)
						const title = blog.title;
						const allText = blog.allText;
						for(var i=0; i<searchArray.length; i++){
							searchStr += str1 + searchArray[i] + str2;
						}
						//console.log(searchStr);
						//console.log(blog.allText)
						matches = (title.match('^.*'+searchStr+'.*$') || allText.match('^.*'+searchStr+'.*$'))
									&& this.search.match(/[ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9]/gi);
						//if(matches!==null) console.log(matches)
						return matches !== null; //if input search matches blog title
					}
				});
			}
		},
		async mounted(){
			//console.log(this.search)
			//console.log(this.filteredSearch)
			this.getBoardCount()
		}
	})
</script>

<style>
#article-content {
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    /* number of lines to show */
    -webkit-box-orient: vertical;
}
</style>