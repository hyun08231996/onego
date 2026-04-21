<template>
	<div style="height:45%;">
	  <div v-if="toggleSignAuto" style="margin-left:8px;position:relative;">
		<v-tooltip left>
		  <template v-slot:activator="{ on, attrs }">
			<v-btn style="position:absolute;right:4px;" @click="showAutocom" icon v-bind="attrs" v-on="on">
			  <v-icon>mdi-chevron-left</v-icon>
			</v-btn>
		  </template>
		  <span>자동완성</span>
		</v-tooltip>
	  </div>
	  <div v-else style="margin-left:8px;position:relative;">
		<span><v-tooltip top v-if="showBtn">
		  <template v-slot:activator="{ on, attrs }">
			<v-btn icon v-bind="attrs" v-on="on" @click="autoComplete"><v-icon>mdi-motion-play-outline</v-icon></v-btn>
		  </template>
		  <span>문장 자동완성</span>
		</v-tooltip>
		<v-progress-circular v-if="isLoading"
			class="ml-2 mt-2 mb-2"
			indeterminate
			width="2"
			size="20"
			color="#00d5aa"/>
		<v-btn @click="clearField" class="ml-1" v-if="suggestions.length!==0" x-small outlined rounded color="grey">지우기</v-btn></span>
		<span style="position:absolute;right:4px;"><v-btn @click="showAutocom" icon><v-icon>mdi-chevron-down</v-icon></v-btn></span>
		<div class="autocom-list">
		  <div v-if="suggestions.length === 0" class="autocom-empty">
			문장 자동완성 버튼을 클릭하면 AI 자동완성 문장이 이곳에 표시됩니다.
		  </div>
		  <v-tooltip
			v-for="(sentence, index) in suggestions"
			:key="`${index}-${sentence}`"
			top>
			<template v-slot:activator="{ on, attrs }">
			  <button
				type="button"
				class="autocom-suggestion-row"
				:class="{ 'autocom-suggestion-row--copied': copiedIndex === index }"
				@click="copySuggestion(sentence, index)"
				v-bind="attrs"
				v-on="on">
				<span class="autocom-suggestion-number">{{ index + 1 }}.</span>
				<span class="autocom-suggestion-text">{{ sentence }}</span>
			  </button>
			</template>
			<span>{{ copiedIndex === index ? 'copied' : 'copy text' }}</span>
		  </v-tooltip>
		</div>
	  </div>
	</div>
</template>

<script lang="ts">
	import { Component, Vue } from 'vue-property-decorator';
	import { namespace } from 'vuex-class';
	import http from '@/http/http-common'
	import { eventBus } from '@/main'

	const WriteStoreModule = namespace('writeStore')

	@Component
	export default class Autocom extends Vue {
		toggleSignAuto = false
		isLoading = false
		showBtn = true
		suggestions:string[] = []
		copiedIndex:number | null = null

		@WriteStoreModule.Getter('getItemList')
		private itemList!:any[]

		@WriteStoreModule.Getter('getActiveVal')
		private activeVal!:number

		showAutocom():void{
			this.toggleSignAuto = !this.toggleSignAuto
		}

		clearField():void{
			this.suggestions = []
			this.copiedIndex = null
		}

		private getCurrentTextSeed():string{
			let content = ''
			if(this.activeVal === 1){
				content = this.itemList[0].text.replaceAll("\n"," ")
			}else if(this.activeVal > 1){
				for(let i=0; i<this.itemList[0].children.length;i++){
					if(this.activeVal === this.itemList[0].children[i].id){
						content = this.itemList[0].children[i].text.replaceAll("\n", " ")
					}
				}
			}
			const sentenceChunks = content.trim().split(/(?<=[.?!])\s+/).filter(Boolean)
			return (sentenceChunks.length > 0 ? sentenceChunks[sentenceChunks.length - 1] : content).trim()
		}

		autoComplete():void{
			this.isLoading = true
			this.showBtn = false

			const form = new FormData()
			const text = this.getCurrentTextSeed()
			form.append('text',text)

			http.
				post('/ai/complete',form)
				.then(response=>{
					if (response.status >=200 && response.status < 204){
						console.log("success")
						this.suggestions = Array.isArray(response.data) ? response.data : []
						this.isLoading = false
						this.showBtn = true
					} else{
						console.log("fail..")
					}
				})
				.catch(() => {
					this.isLoading = false
					this.showBtn = true
				})
			
		}

		private copyText(text:string):void{
			if(navigator.clipboard && navigator.clipboard.writeText){
				navigator.clipboard.writeText(text)
				return
			}
			const textarea = document.createElement('textarea')
			textarea.value = text
			document.body.appendChild(textarea)
			textarea.select()
			document.execCommand('copy')
			document.body.removeChild(textarea)
		}

		copySuggestion(sentence:string, index:number):void{
			const copyText = sentence.replace(/^\s*\d+[.)]?\s*/, '').trim()
			this.copyText(copyText)
			this.copiedIndex = index
			window.setTimeout(() => {
				if(this.copiedIndex === index){
					this.copiedIndex = null
				}
			}, 1200)
		}

		private handleAutocompleteResults = (results:string[]):void => {
			this.suggestions = results
			this.showBtn = true
		}

		private handleAutocompleteLoading = (loading:boolean):void => {
			this.isLoading = loading
		}

		created():void{
			eventBus.$on('autocompleteResults', this.handleAutocompleteResults)
			eventBus.$on('autocompleteLoading', this.handleAutocompleteLoading)
		}

		beforeDestroy():void{
			eventBus.$off('autocompleteResults', this.handleAutocompleteResults)
			eventBus.$off('autocompleteLoading', this.handleAutocompleteLoading)
		}
	}
</script>

<style scoped>
.autocom-list{
	margin-left:8px;
	margin-right:14px;
	margin-top:10px;
	display:flex;
	flex-direction:column;
	gap:8px;
	max-height:32vh;
	overflow:auto;
}

.autocom-empty{
	padding:14px 12px;
	border:1px dashed rgba(0, 0, 0, 0.12);
	border-radius:10px;
	color:#8b8b8b;
	font-size:0.92rem;
	background:#fafafa;
}

.autocom-suggestion-row{
	display:flex;
	align-items:flex-start;
	gap:8px;
	width:100%;
	padding:12px 14px;
	border:1px solid rgba(0, 213, 170, 0.16);
	border-radius:12px;
	background:white;
	text-align:left;
	transition: color 0.18s ease, background-color 0.18s ease, border-color 0.18s ease, transform 0.18s ease;
	color:#4e4e4e;
}

.autocom-suggestion-row:hover{
	color:#00a886;
	background:rgba(0, 213, 170, 0.06);
	border-color:rgba(0, 213, 170, 0.42);
	transform:translateY(-1px);
}

.autocom-suggestion-row--copied{
	color:#00997b;
	background:rgba(0, 213, 170, 0.10);
}

.autocom-suggestion-number{
	flex:0 0 auto;
	font-weight:700;
}

.autocom-suggestion-text{
	flex:1 1 auto;
	line-height:1.45;
}

</style>
