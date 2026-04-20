<template>
  <v-row id="modal-margin" class="mx-auto justify-center">
	<!-- modal -->
    <v-dialog
      v-model="dialog"
      fullscreen
      hide-overlay
	  persistent
      transition="dialog-bottom-transition"
    >
	  <!-- magnify button click shows modal -->
	  <template v-slot:activator="{ on, attrs }">
		<v-btn icon
			v-bind="attrs"
          	v-on="on"
			@click="getUsersAndBoards">
			<v-icon>mdi-magnify</v-icon>
		</v-btn>
	  </template>

      <v-card>
		<!-- header -->
        <v-toolbar
          color="white" fixed elevation="0"
        >
          <v-app-bar-nav-icon @click="openDrawer"></v-app-bar-nav-icon>

		  <a href="/"><img src="@/assets/logo/onego_logo.jpeg"
		  	width="120px" height="43.2px"
			style="vertical-align:middle;"></a>
          <v-spacer></v-spacer>
          <v-btn
            icon
            @click="dialog = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
		<v-flex id="text-field-container" class="mx-auto justify-center">
			<!-- search bar -->
			<v-text-field id="text-field" class="text_field"
				v-model="search"
				color="#00d5aa"
				height="50px"
				placeholder="검색어를 입력하세요"
				single-line
				autofocus
				:append-icon="'mdi-magnify'"
				@click:append="doSearch"
				@keyup.enter="doSearch"
				@keyup="hideTable">
			</v-text-field>
			<!-- search list -->
			<div id="search-list" v-if="isSearch">
				<v-card class="mx-auto" tile>
					<v-list dense>
						<div v-if="filteredSearch.length===0 && search!==''">
							<v-card-text>검색 결과가 없습니다.</v-card-text>
						</div>
						<v-list-item
							:key="i" v-for="(blog, i) in filteredSearch.slice(0,8)"><!-- shows only 8 search results from filteredSearch -->
							<a @click="openArticle(blog.id)" id="blog-item" class='a-tag' v-html="highlight(blog.title)"><!-- v-html="highlight(blog.title)" -->
								<v-list-item-content>{{blog.title}}</v-list-item-content></a>
						</v-list-item>
					</v-list>
				</v-card>
			</div>
		</v-flex>
		<!-- user list -->
		<!-- <div align="center" id="table-container" v-if="isTable">
			<v-simple-table style="text-align:center;">
				<tr>
					<td v-for="user in userList" :key="user.name">
						<a href="#" id="user-item" class='a-tag'>
							<v-list-item-avatar size=100 class="mx-auto" id="user-img-div">
								<img :src="user.img" id="user-img">
							</v-list-item-avatar>
							<v-list-item-content>
								<v-list-item-title id="user-name">{{user.name}}</v-list-item-title>
							</v-list-item-content>
							<div><div id="user-intro">{{user.intro}}</div></div>
						</a>
					</td>
				</tr>
			</v-simple-table>
		</div> -->

      </v-card>

    </v-dialog>
  </v-row>
</template>

<script lang="ts">
	import Vue from 'vue'
	import '@/assets/css/SearchModal.css'
	import http from '@/http/http-common'

	declare interface BlogList {
		id:string,
		title:string,
		allText:string,
		nickname:string,
		content:string,
		date:string
	}

	export default Vue.extend({

		data: ()=>({
			errored:false,
			loading:true,
			totalPageNum:1,
			search: '',
			isSearch: false,
			isTable: true,
			dialog: false,
			notifications: false,
			sound: true,
			widgets: false,
			// userList:[],//get 5 random users from db
			blogList:[] as BlogList[]
		}),
		components: {
		},
		methods: {
			openDrawer(){
				this.$emit('openDrawer', true);
			},
			doSearch(){
				if(this.search == ""){
					alert("검색어를 입력해주세요.");
					return;
				}
				location.href = "/search/"+this.search;
			},
			hideTable(){
				if(this.search != ""){
					this.isTable = false;
					this.isSearch = true;
				}else if(this.search == ""){
					this.isTable = true;
					this.isSearch = false;
				}
			},
			highlight(title:string){
				const searchWord1 = this.search.replace(/\s/g, "").split("").join('|'); //
				const searchWord2 = this.search.split(" ").join('|');
				return title.replace(new RegExp(searchWord1, "gi"), match => {
					return '<span class="highlight">' + match + '</span>'; //replaces this.search with highlighted this.search
				}) && title.replace(new RegExp(searchWord2, "gi"), match => {
					return '<span class="highlight">' + match + '</span>';
				});
			},
			async getUsersAndBoards(){
				// await http.
				//     get('/users', )
				await http.
					get('/board/count',{
						// headers:{
						// 	'Authorization': 'Bearer '+localStorage.getItem('accessToken')
						// }
					})
					.then(response => {
						//console.log(response.data)
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
					headers:{
						'Authorization': 'Bearer '+localStorage.getItem('accessToken')
					}
				})
				.then(response => {
					//console.log(pageNum)
					for(let i=0; i<response.data.length;i++){
						//console.log(i)
						const id = response.data[i].id
						const nickname = response.data[i].nickName
						const title = response.data[i].title
						const content = response.data[i].contents[0].content
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
						this.blogList.push({id:id,nickname:nickname,title:title,allText:allText,content:content,date:date})
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
				//console.log(searchArray);
				//console.log(searchWord1);
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

	})
</script>

<style>

</style>