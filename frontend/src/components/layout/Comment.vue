<template>
  <v-card
    max-width="50%"
    flat
    id="comment"
  >
    <h3>댓글</h3>
    <br/><hr style="margin: auto;"><br/>

    <div class="content" v-for="(item, i) in commentList" :key="i">

        <span class="nickname"> {{ item.nickName }}</span>
        <span class="modDatetime">{{ item.modDatetime }}</span>

        <template v-if="item.edited===true">
          <span class="comment-btn" v-if="$store.state.user.userAccount.attributes.email === item.userId">
          <v-btn
          depressed
          small
          @click = "putComment(boardId,item.id,item.userId,item.nickName,comment2)"
          >
          확인</v-btn></span>
          <textarea
          v-model="comment2"
          class="new_comment"
          max="300"
          ></textarea>
        </template>

        <template v-else>
        <span class="comment-btn" v-if="$store.state.user.userAccount.attributes.email === item.userId">
          <v-btn
          small
          depressed
          @click = "deleteComment(boardId,item.id)"
          >
        삭제</v-btn></span>

        <span class="comment-btn" v-if="$store.state.user.userAccount.attributes.email === item.userId">
          <v-btn
          depressed
          small
          @click = "editedComment(i)"
          >
        수정</v-btn></span>

        <p class="comment">{{ item.comment }}</p>

        </template>
       </div>

      <div class="content">
      <textarea
        v-model="comment"
        class="new_comment"
        placeholder="댓글을 입력해주세요!"
        max="300"
      ></textarea>
      <button
        type="submit"
        @click = "submit"
      >등록</button>
      </div>
  </v-card>
</template>


<script lang="ts">

import Vue from 'vue'
import http from '../../http/http-common'


declare interface CommentList{
  comment2:string,
	comment:string,
	id:string,
	modDatetime:Date,
	nickName:string,
	userId:string
}

export default Vue.extend({

    props: {
        boardId: String,
    },
    data: () => ({
        commentList: [] as CommentList[],
        nickName: '',
        comment: '',
        comment2:'',
        pageNumber: '',
        userId: ''
    }),

    methods: {
        //댓글 불러오기
        async getComment(boardId: string, pageNumber: number){
        await http
            .get('/comment', {
            params: { 'boardId': boardId, 'pageNumber': pageNumber },
            headers:{
                      'Authorization': 'Bearer '+localStorage.getItem('accessToken')
                    }}) 
            .then(response => {
                this.commentList = response.data
            })
        },

        //댓글 산입하기
        submit(){
            if(this.$store.state.user.signedIn==true){
                this.insertComment(
                  this.$route.params.boardId, this.$store.state.user.userAccount.attributes.nickname,
                  this.comment, this.$store.state.user.userAccount.attributes.email
                )
              }
            else{
              alert("로그인부터 해주세요!")
            }
        },

        insertComment(boardId: string, nickName: string, comment:string, userId:string){
                    http
                    .post('/comment', {
                      'boardId': boardId, 'nickName': nickName, 'comment': comment, 'userId': userId
                    },
                    {headers:{
                      'Authorization': 'Bearer '+localStorage.getItem('accessToken')
                    }})
                    .then(response => {
                        this.getComment(this.$route.params.boardId, 1)
                    })
        },

        editedComment(index:number){
            this.$set(this.commentList[index],'edited',true)
        },

        putComment( boardId:string, commentId:string, userId:string, nickName:string, comment:string){
                    http
                    .put('/comment', {
                      'boardId': boardId, 'commentId': commentId, 'userId': userId, 'nickName': nickName, 'comment': comment,
                      },
                      {headers:{
                        'Authorization': 'Bearer '+localStorage.getItem('accessToken')
                      }})
                    .then(response => {
                        this.getComment(this.$route.params.boardId, 1)
                    }).catch(c => {
                      console.log(c)} )
                                 
            },

        //댓글 삭제하기
        deleteComment(boardId: string, commentId: string){
                    http
                    .delete('/comment', {
                    data: { 'boardId': boardId, 'commentId': commentId}, 
                    headers:{
                        'Authorization': 'Bearer '+localStorage.getItem('accessToken')
                    }})
                    .then(response => {
                        this.getComment(this.$route.params.boardId, 1)
                    })
            },


    },
    created(){
		this.getComment(this.$route.params.boardId, 1)
    },
})
</script>

<style>
#comment{
  margin: auto;
  width: 96%;
  min-height: 100px;
}
.content{
  margin: auto;
  width: 90%;
  height: 100px;
}
.img-box{
  width: 60px;
  height: 60px;
  border-radius: 70%;
  overflow: hidden;
  float:left;
  margin-top: 15px;
  margin-bottom: 20px;
  margin-left: 20px;
}
.img{
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.nickname{
   font-family: Noto Sans KR;
   font-size : 1.25rem;
   font-weight: 500;
   width: 80%;
   height: 35px;
   padding-top: 10px;
}
.comment{
  font-family: Noto Sans KR;
  font-size : 1rem;
  font-weight: 300;
  padding-top: 5px;
  padding-bottom: 10px;
}
.modDatetime{
  padding-left: 10px;
  font-weight: 200;
}
.text{
  width: 100%;
}
.comment-btn{
  vertical-align: middle;
  float: right;
}
.form{
  width: 100%;
  margin-left: 100px;
}
.new_comment{
 width: 94%;
 margin-right:10px;
 height: 20px;
}
</style>
