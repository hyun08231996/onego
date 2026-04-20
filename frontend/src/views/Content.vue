<template>
  <div id="textArea">
    <!-- contents -->
    <div id="Posts">
         <Post />
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import VueRouter from 'vue-router'
import http from '@/http/http-common'

Vue.use(VueRouter)

  import Post from '../components/layout/Post.vue'
  import { eventBus } from '@/main'

  export default Vue.extend({
    props:{
      boardId:String
    },
		data: () => ({
      errored:false,
      loading:true
		}),
		name: "Header",
		components:{
			Post,
		},
    methods:{
      async getUserEmail(){
        http.
          get('/board',{
            params:{'boardId':this.boardId}
          })
          .then(response => {
            //console.log(response.data[0].userEmail)
            if(this.$store.state.user.userAccount.attributes.email === response.data[0].userEmail){
              eventBus.$emit('sameAuthor',true)
              //console.log(this.boardId)
              eventBus.$emit('boardId',this.boardId)
            }
          })
          .catch(() => this.errored = true )
          .finally(() => this.loading = false)
      }
    },
    created(){
      //console.log(this.boardId)
      this.getUserEmail()
    }
	})

</script>
<style>

</style>