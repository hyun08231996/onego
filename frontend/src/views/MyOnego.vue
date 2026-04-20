<template>
  <div>
    <v-flex id="myonego-margin" class="mx-auto">
	  <div align="center" class="spacing">
		<a href="#saved" id="saved-btn" @click="showSaved"><label id="saved-label">저장글</label></a>&nbsp;&nbsp;&nbsp;
		<a href="#posted" id="posted-btn" @click="showPosted"><label id="posted-label">발행글</label></a>
	  </div>
	  <br>
	  <!-- 저장글 -->
	  <div v-if="isSaved">
		<div v-if="savedList.length === 0">
			<div align="center" style="font-size:1rem;opacity:60%;margin-top:90px;">저장된 글이 없습니다.</div>
		</div>
		<div v-else>
	      <div v-for="(article,i) in savedList" :key="i">
			<a class="edit-article" @click="editDraft(article.id)">
			  <div>
		      <div class="article-title" style="font-size:1.35rem;">{{article.title}}</div>
		      <div class="article-text">{{article.text}}</div><br>
			  <div style="font-size:0.8rem;opacity:50%">{{article.date}}</div>
			  </div>
			</a>
			<v-divider class="divider-myonego"/>
	      </div>
		</div>
	  </div>
	  <!-- 발행글 -->
	  <div v-if="isPosted">
		<div v-if="postedList.length === 0">
			<div align="center" style="font-size:1rem;opacity:60%;margin-top:90px;">발행된 글이 없습니다.</div>
		</div>
		<div v-else>
	      <div v-for="(article,i) in postedList" :key="i">
			<a class="edit-article" @click="openArticle(article.id)">
			  <div>
		      <div class="article-title" style="font-size:1.35rem;">{{article.title}}</div>
		      <div class="article-text">{{article.text}}</div><br>
			  <div style="font-size:0.8rem;opacity:50%">{{article.date}}</div>
			  </div>
			</a>
			<v-divider class="divider-myonego"/>
	      </div>
		</div>
	  </div>
	</v-flex>
  </div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import http from '@/http/http-common'

	declare interface SavedList {
		id:string,
		title:string,
		text:string,
		date:string,
		dateTime:Date
	}

	declare interface PostedList {
		id:string,
		title:string,
		text:string,
		date:string,
		dateTime:Date
	}

	@Component
	export default class MyOnego extends Vue{
		errored = false
		loading = true
		savedList : SavedList[] = []
		postedList : PostedList[] = []
		isSaved = true
		isPosted = false
		savedPagenum = 1
		postedPagenum = 1

		async created(){
			this.tempBoardCount()
			this.boardCount()
		}

		showSaved(){
			this.isSaved = true;
			this.isPosted = false;
			document.getElementById('posted-label')!.style.color = "#9E9E9E";
			document.getElementById('posted-label')!.style.textDecoration = "none";
			document.getElementById('saved-label')!.style.color = "#00d5aa";
			document.getElementById('saved-label')!.style.textDecoration = "underline";
		}
		showPosted(){
			this.isSaved = false;
			this.isPosted = true;
			document.getElementById('saved-label')!.style.color = "#9E9E9E";
			document.getElementById('saved-label')!.style.textDecoration = "none";
			document.getElementById('posted-label')!.style.color = "#00d5aa";
			document.getElementById('posted-label')!.style.textDecoration = "underline";
		}
		async tempBoardCount(){
         await http
             .get('/tempBoard/count', {
				 params:{
					 'userEmail':this.$store.state.user.userAccount.attributes.email
				 },
				 headers:{
					'Authorization': 'Bearer '+localStorage.getItem('accessToken')
				 }
			 })
             .then(response => {
				 //console.log('tempBoard: '+response.data)
				 this.savedPagenum = Math.ceil(response.data / 5)
				 for(let i=1; i<=this.savedPagenum;i++){
					this.getAllSaved(i)
				 }
             })
             .catch(() => this.errored = true )
             .finally(() => this.loading = false)
        }
		async boardCount(){
         await http
             .get('/board/count', {
				 params:{
					 'userEmail':this.$store.state.user.userAccount.attributes.email
				 },
				//  headers:{
				// 	'Authorization': 'Bearer '+localStorage.getItem('accessToken')
				//  }
			 })
             .then(response => {
				 //console.log('board: '+response.data)
				 this.postedPagenum = Math.ceil(response.data / 5)
				 for(let j=1; j<=this.postedPagenum;j++){
					this.getAllPosted(j)
				 }
             })
             .catch(() => this.errored = true )
             .finally(() => this.loading = false)
        }
		async getAllSaved(pageNum:number){
			await http.
				get('/tempBoard',{
					params:{
						'userEmail': this.$store.state.user.userAccount.attributes.email,
						'pageNumber':pageNum
					},
					headers:{
						'Authorization': 'Bearer '+localStorage.getItem('accessToken')
					}
				})
				.then(response => {
					//console.log(response.data)
					for(var i=0; i<response.data.length;i++){
						//console.log(response.data[i].id)
						const id = response.data[i].id
						const title = response.data[i].title
						const text = response.data[i].contents[0].content
						const dateTime = new Date(response.data[i].modDatetime)
						var mm = dateTime.getMonth() + 1 // getMonth() is zero-based
						var dd = dateTime.getDate()
						const date = [dateTime.getFullYear(),
										(mm>9 ? '' : '0') + mm,
										(dd>9 ? '' : '0') + dd
										].join('.')
						//console.log(title,text,date)
						this.savedList.push({id:id, title:title,text:text,date:date,dateTime:dateTime})
					}
					this.savedList.sort((a,b)=>b.dateTime.getTime()-a.dateTime.getTime())
				})
				.catch(() => this.errored = true )
				.finally(() => {
					this.loading = false
				})
		}
		async getAllPosted(pageNum:number){
			await http.
				get('/board',{
					params:{
						'userEmail': this.$store.state.user.userAccount.attributes.email,
						'pageNumber':pageNum
					},
					headers:{
						'Authorization': 'Bearer '+localStorage.getItem('accessToken')
					}
				})
				.then(response => {
					//console.log(response.data)
					for(var i=0; i<response.data.length;i++){
						//console.log(response.data)
						const id = response.data[i].id
						const title = response.data[i].title
						const text = response.data[i].contents[0].content
						const dateTime = new Date(response.data[i].modDatetime)
						var mm = dateTime.getMonth() + 1 // getMonth() is zero-based
						var dd = dateTime.getDate()
						const date = [dateTime.getFullYear(),
										(mm>9 ? '' : '0') + mm,
										(dd>9 ? '' : '0') + dd
										].join('.')
						//console.log(title,text,date)
						if(response.data[i].userEmail!==null && response.data[i].userEmail == this.$store.state.user.userAccount.attributes.email)
							this.postedList.push({id:id, title:title,text:text,date:date,dateTime:dateTime})
					}
					this.postedList.sort((a,b)=>b.dateTime.getTime()-a.dateTime.getTime())
				})
				.catch(() => this.errored = true )
				.finally(() => {
					this.loading = false
				})
		}

		editDraft(tempBoardId:string){
			window.open('/write/'+tempBoardId,'_self')
		}

		openArticle(boardId:string){
			window.open('/content/'+boardId,'_self')
		}
	}
</script>

<style>
#myonego-margin{
	max-width:55%;
	margin-top: -25px;
}
#saved-label{
	color:#00d5aa;
	text-decoration: underline;
}
#posted-label{
	color:#9E9E9E;
}
#saved-btn:hover > #saved-label,
#posted-btn:hover > #posted-label{
	cursor:pointer !important;
	text-decoration:underline !important;
	color: #00d5aa !important;
}
.divider-myonego{
	margin-top:30px;
	margin-bottom: 30px;
}
.edit-article,#saved-btn,#posted-btn{
	text-decoration: none !important;
	color: black !important;
}
.edit-article:hover .article-title{
	text-decoration:underline !important;
	color: #00d5aa !important;
}
.article-text{
	font-size:1rem;
	opacity:60%;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 1;
    /* number of lines to show */
    -webkit-box-orient: vertical;
}
</style>