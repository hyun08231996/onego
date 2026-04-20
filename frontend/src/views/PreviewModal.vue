<template>
  <v-row class="mx-auto justify-center">
	<!-- modal -->
    <v-dialog
      v-model="dialog"
      fullscreen
	  persistent
      transition="dialog-transition"
    >
	  <!-- preview button click shows modal -->
	  <template v-slot:activator="{ on, attrs }">
		<v-btn id="preview-btn" class="ma-2"
			rounded outlined color="grey"
			v-bind="attrs"
          	v-on="on"
			@click="getCurDate">
			미리보기
		</v-btn>
	  </template>

      <v-card>
		<!-- header -->
        <v-toolbar
          color="transparent" fixed elevation="0"
        >
		  <v-spacer/>
          <v-btn
            icon
			right
            @click="dialog = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>
		<!-- Title Image -->
		<v-card tile v-if="imageUrl !== ''" class="mb-12" id="image-card">
			  <v-img height="50vh"  :src="imageUrl">
				  <v-flex id="title-preview-margin" class="mx-auto">
					<h1 style="font-size:40px;" v-html="itemList[0].title"></h1>
					<div style="opacity:80%;"><h3 v-html="itemList[0].subtitle"></h3></div>
					<div style="opacity:60%;margin-top:30px;"><h5>{{this.$store.state.user.userAccount.attributes.nickname}} · {{date}}</h5></div>
				  </v-flex>
			  </v-img>
		</v-card>

		<!--Title content-->
		<v-flex v-if="imageUrl == ''" id="title-content-preview-margin" class="mx-auto mb-12">
			<h1 style="font-size:40px;" v-html="itemList[0].title"></h1>
			<div style="opacity:80%;"><h3 v-html="itemList[0].subtitle"></h3></div>
			<div style="opacity:60%;margin-top:30px;"><h5>{{this.$store.state.user.userAccount.attributes.nickname}} · {{date}}</h5></div>
		</v-flex>

		<!-- Content -->
		<v-flex id="content-preview-margin" class="mx-auto">
			<div>
				<p v-html="itemList[0].text"></p>
			</div>
			<div v-if="itemList[0].children.length!==0">
			  <div v-for="(content,i) in itemList[0].children" :key="i">
				<h3 v-html="content.subtitle"></h3>
				<p v-html="content.text"></p>
			  </div>
			</div>
		</v-flex>

		<!-- Tags -->
		<v-flex id="tag-preview-margin" class="mx-auto mt-8 pb-8">
			<span v-for="(tag,i) in tagList" :key="i">
				<v-chip outlined small color="#00d5aa" class="mr-2">{{tag}}</v-chip>
			</span>
		</v-flex>

      </v-card>

    </v-dialog>
  </v-row>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import { namespace } from 'vuex-class';

	const WriteStoreModule = namespace('writeStore')

	@Component
	export default class PreviewModal extends Vue {
		dialog = false
		date = ''

		@WriteStoreModule.State('imageUrl')
		private imageUrl!:string

		@WriteStoreModule.State('modDatetime')
		private dateTime!:Date

		@WriteStoreModule.State('tagList')
		private tagList!:string[]

		@WriteStoreModule.Mutation('setDate')
		private setDate!:(date:Date)=>void

		@WriteStoreModule.Getter('getItemList')
		private itemList!:any[]

		mounted(){
			var mm = this.dateTime.getMonth() + 1 // getMonth() is zero-based
			var dd = this.dateTime.getDate()

			const date = [this.dateTime.getFullYear(),
						(mm>9 ? '' : '0') + mm,
						(dd>9 ? '' : '0') + dd
						].join('.')
			this.date = date
		}

		getCurDate():void{
			const date = new Date()
			this.setDate(date)
		}

	}
</script>

<style>
#preview-btn:hover{
	color:#757575 !important;
}
#image-card{
	position:relative !important;
}
#title-preview-margin{
	max-width:50% !important;
	position:absolute !important;
	bottom:10% !important;
	left:25% !important;
}
#image-card .v-image__image{
	opacity:0.7 !important;
}
#title-content-preview-margin,
#content-preview-margin,
#tag-preview-margin{
	max-width:50% !important;
}
</style>