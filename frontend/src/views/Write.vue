<template>
  <div style="margin-bottom:-400px;">
	<div style="margin-top:-36px;"><v-divider/></div>
	<!-- 목록 -->
	<treeview :tempBoardId="tempBoardId"/>

	<div align="center" id="write-margin" >
		<div id="editor-size">

		  <div style="width:100%;float:left;">
			  <v-card class="title-card" height="6.1vh" elevation="2" :color="isDark?'#282828':'#f5f5f5'">
				<!-- 제목 -->
				<div style="width:50%;height:6.1vh;padding-top:4px;padding-bottom:4px;float:left;">
				  <v-text-field class="mx-2"
				    v-model="title"
				  	height="5.1vh"
					color="#00d5aa"
					:background-color="isDark?'#1e1e1e':'white'"
					:placeholder="titlePlace"
					:label="titleLabel"
					dense outlined/>
				</div>
				<!-- 소제목 -->
				<div style="width:50%;height:6.1vh;padding-top:4px;padding-bottom:4px;float:left;">
					
					
				  <v-text-field class="mx-2"
				    v-model="subtitle"
				  	height="5.1vh"
					color="#00d5aa"
					:background-color="isDark?'#1e1e1e':'white'"
					:placeholder="subtitlePlace"
					:label="subtitleLabel"
					dense outlined>
					<template v-slot:append-outer v-if="activeVal === 1">
					  <v-hover v-slot="{ hover }">
						<v-tooltip top>
							<template v-slot:activator="{ on, attrs }">
								<v-btn icon :color="hover ? '#00d5aa' : ''" v-bind="attrs" v-on="on" @click="generateSub"><v-icon>mdi-clipboard-text-play-outline</v-icon></v-btn>
							</template>
							<span>소제목 자동생성</span>
				        </v-tooltip>
					  </v-hover>
					</template>
				  </v-text-field>
				  <v-progress-linear v-if="isLoading"
					indeterminate
					absolute
					height="2"
					color="#00d5aa"/>
				</div>
			  </v-card>
		  </div>
		  <!-- 텍스트 에디터 -->
		  <div style="width:100%;float:left;position:relative;" ref="editorShell">
			<tiptap-vuetify id="text-editor"
				@keydown.native.capture="handleEditorKeydown"
				v-model="content"
				:toolbar-attributes="{ color: isDark?'#282828':'#f5f5f5' }"
				:extensions="extensions"
				:native-extensions="nativeExtensions"
				:disabled="isActive"
				autoFocus=true
				placeholder="글 내용을 입력하세요"
				>
			</tiptap-vuetify>
			<div
				v-if="showInlineSuggestionBubble"
				ref="inlineSuggestionBubble"
				class="inline-autocomplete-bubble"
				:class="{ 'inline-autocomplete-bubble--dark': isDark }"
				:style="inlineSuggestionStyle"
				@click="acceptInlineSuggestion">
				<div v-if="isInlineLoading" class="inline-autocomplete-hint">AI가 문장을 이어 쓰는 중...</div>
				<div v-else class="inline-autocomplete-suggestion">
					<span class="inline-autocomplete-label">Tab</span>
					<span class="inline-autocomplete-text">{{ inlineSuggestionSuffix }}</span>
				</div>
			</div>
		  </div>
		  <!-- 태그 입력, 이미지 선택, 글자수 -->
		  <tag />
		</div>
	</div>
	<!-- 자동완성 & 메모 -->
	<div id="memo-margin">
		<div id="memo-size">
		  <!-- 자동완성 -->
		  <autocom />
		  <v-divider style="margin-bottom:7px;"/>
		  <!-- 메모 -->
		  <memo />
		</div>
	</div>
  </div>
</template>

<script lang="ts">
	import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
	// eslint-disable-next-line @typescript-eslint/ban-ts-comment
	// @ts-ignore
	import { TiptapVuetify, History, Paragraph, Heading, Bold, Italic, Underline } from "tiptap-vuetify";
	import Treeview from '@/components/layout/write/Treeview.vue'
	import Autocom from '@/components/layout/write/Autocom.vue'
	import Memo from '@/components/layout/write/Memo.vue'
	import Tag from '@/components/layout/write/Tag.vue'
	import '@/assets/css/Write.css'
	import { namespace } from 'vuex-class';
	import http from '@/http/http-common'
	import { eventBus } from '@/main'

	const WriteStoreModule = namespace('writeStore')

	@Component({
		components:{
			TiptapVuetify,
			'treeview':Treeview,
			'autocom':Autocom,
			'memo':Memo,
			'tag':Tag
		}

	})
	export default class Write extends Vue {
		@Prop({ type: String }) readonly tempBoardId!: string
		@Prop({ type: String }) readonly boardId!: string

		extensions : unknown = [
			History,
			Paragraph,
			[Heading, { options: {levels:[1,2,3]}}],
			Bold,
			Italic,
			Underline
		]
		nativeExtensions : unknown = []
		titleLabel = '글 제목'
		subtitleLabel = '글 소제목'
		titlePlace = '글 제목을 입력하세요'
		subtitlePlace = '글 소제목을 입력하세요'
		title = ''
		subtitle = ''
		errored = false
		loading = true
		content = ''
		isActive = false
		isLoading = false
		isDark = false
		inlineSuggestion = ''
		inlineSuggestionSuffix = ''
		isInlineLoading = false
		inlineSuggestionTop = 0
		inlineSuggestionLeft = 0
		inlineSuggestionVisible = false
		private autocompleteTimer: ReturnType<typeof setTimeout> | null = null
		private autocompleteRequestId = 0
		private suppressAutocomplete = false

		@Watch('activeVal')
		watchActiveVal():void{
			//console.log(this.activeVal)
			if(this.activeVal == undefined){
				this.isActive = true
			}else this.isActive = false

			if(this.activeVal > 1){
				this.titleLabel = '목차 이름'
				this.subtitleLabel = '목차 소제목'
				this.titlePlace = '목차 이름을 입력하세요'
				this.subtitlePlace = '목차 소제목을 입력하세요'
			}else if(this.activeVal === 1){
				this.titleLabel = '글 제목'
				this.subtitleLabel = '글 소제목'
				this.titlePlace = '글 제목을 입력하세요'
				this.subtitlePlace = '글 소제목을 입력하세요'
			}
		}

		@Watch('getContent')
		watchGetContent():void{
			this.content = this.getContent
			this.updateContent(this.content)
		}

		@Watch('content')
		watchContent():void{
			//console.log(this.content)
			this.setContent(this.content)
			this.updateContent(this.content)
			if(this.suppressAutocomplete){
				this.suppressAutocomplete = false
				return
			}
			this.scheduleInlineAutocomplete()
		}

		@Watch('getTitle')
		watchGetTitle():void{
			this.title = this.getTitle
			this.updateTitle(this.title)
		}

		@Watch('title')
		watchTitle():void{
			this.setTitle(this.title)
			this.updateTitle(this.title)
		}

		@Watch('getSubtitle')
		watchGetSubtitle():void{
			this.subtitle = this.getSubtitle
			this.updateSubtitle(this.subtitle)
		}

		@Watch('subtitle')
		watchSubtitle():void{
			this.setSubtitle(this.subtitle)
			this.updateSubtitle(this.subtitle)
		}

		@WriteStoreModule.Getter('getId') private getId!:string

		@WriteStoreModule.Getter('getContent') private getContent!:string

		@WriteStoreModule.Mutation('setContent') private setContent!:(data:string)=>void

		@WriteStoreModule.Mutation('updateContent') private updateContent!:(data:string)=>void

		@WriteStoreModule.Getter('getTitle') private getTitle!:string

		@WriteStoreModule.Mutation('setTitle') private setTitle!:(data:string)=>void

		@WriteStoreModule.Mutation('updateTitle') private updateTitle!:(data:string)=>void

		@WriteStoreModule.Getter('getSubtitle') private getSubtitle!:string

		@WriteStoreModule.Mutation('setSubtitle') private setSubtitle!:(data:string)=>void

		@WriteStoreModule.Mutation('updateSubtitle') private updateSubtitle!:(data:string)=>void

		@WriteStoreModule.Getter('getActiveVal') private activeVal!:number

		@WriteStoreModule.Mutation('setId') private setId!:(tempBoardId:string)=>void

		@WriteStoreModule.Mutation('setMemoList') private setMemoList!:(list:any[])=>void

		@WriteStoreModule.Mutation('setTagList') private setTagList!:(list:string[])=>void

		@WriteStoreModule.Mutation('setItemList') private setItemList!:(list:any[])=>void

		@WriteStoreModule.Mutation('setMainTitle') private setMainTitle!:(title:string)=>void

		@WriteStoreModule.Mutation('setMainSubtitle') private setMainSubtitle!:(subtitle:string)=>void

		@WriteStoreModule.Mutation('setImageUrl') private setImageUrl!:(url:string)=>void

		@WriteStoreModule.Getter('getItemList') private itemList!:any[]

		created(){
			eventBus.$on('toDark', (val:boolean)=>{this.isDark=val;})
			eventBus.$on('toLight', (val:boolean)=>{this.isDark=val;})
			history.pushState(null, '', document.URL)
			window.onpopstate = () => {
				this.confirmBack()
				history.pushState(null, '', document.URL)
			}
			if(this.tempBoardId !== undefined && this.boardId == undefined) this.editTempBoard(this.tempBoardId)
			if(this.boardId !== undefined && this.tempBoardId == undefined) this.editBoard(this.boardId)
			//this.content = this.getContent
			//console.log(this.getId)
		}

		mounted():void{
			document.addEventListener('selectionchange', this.handleSelectionChange)
		}

		beforeDestroy():void{
			document.removeEventListener('selectionchange', this.handleSelectionChange)
			if(this.autocompleteTimer){
				clearTimeout(this.autocompleteTimer)
			}
		}

		get showInlineSuggestionBubble():boolean{
			return this.inlineSuggestionVisible && (this.isInlineLoading || this.inlineSuggestionSuffix.length > 0)
		}

		get inlineSuggestionStyle():Record<string, string>{
			const bubbleWidth = 360
			return {
				top: `${this.inlineSuggestionTop}px`,
				left: `${this.inlineSuggestionLeft}px`,
				width: `${bubbleWidth}px`,
			}
		}

		private getActivePlainText():string{
			if(this.activeVal === 1){
				return this.itemList[0]?.text || ''
			}
			if(this.activeVal > 1){
				for(let i=0; i<this.itemList[0].children.length; i++){
					if(this.activeVal === this.itemList[0].children[i].id){
						return this.itemList[0].children[i].text || ''
					}
				}
			}
			return ''
		}

		private getActiveSentenceSeed():string{
			const plainText = this.getActivePlainText().replaceAll('\n', ' ').trim()
			if(plainText.length === 0){
				return ''
			}
			const sentenceChunks = plainText.split(/(?<=[.?!])\s+/).filter(Boolean)
			const lastSentence = sentenceChunks.length > 0 ? sentenceChunks[sentenceChunks.length - 1] : plainText
			return lastSentence.trim()
		}

		private emitAutocompleteState(suggestions:string[], loading:boolean):void{
			eventBus.$emit('autocompleteResults', suggestions)
			eventBus.$emit('autocompleteLoading', loading)
		}

		private clearInlineSuggestion():void{
			this.inlineSuggestion = ''
			this.inlineSuggestionSuffix = ''
			this.isInlineLoading = false
			this.inlineSuggestionVisible = false
			this.emitAutocompleteState([], false)
		}

		private buildSuggestionSuffix(seed:string, suggestion:string):string{
			const normalizedSeed = seed.trim()
			const normalizedSuggestion = suggestion.trim()
			if(!normalizedSuggestion){
				return ''
			}
			if(normalizedSeed && normalizedSuggestion.startsWith(normalizedSeed)){
				return normalizedSuggestion.slice(normalizedSeed.length).trimStart()
			}

			const maxOverlap = Math.min(normalizedSeed.length, normalizedSuggestion.length)
			for(let overlap = maxOverlap; overlap > 0; overlap--){
				const seedTail = normalizedSeed.slice(-overlap)
				const suggestionHead = normalizedSuggestion.slice(0, overlap)
				if(seedTail === suggestionHead){
					return normalizedSuggestion.slice(overlap).trimStart()
				}
			}
			return normalizedSuggestion
		}

		private updateInlineSuggestionPosition():void{
			if(!this.isEditorFocused() || (!this.isInlineLoading && !this.inlineSuggestionSuffix)){
				this.inlineSuggestionVisible = false
				return
			}

			const selection = window.getSelection()
			const editorShell = this.$refs.editorShell as HTMLElement | undefined
			if(!selection || selection.rangeCount === 0 || !editorShell){
				this.inlineSuggestionVisible = false
				return
			}

			const range = selection.getRangeAt(0).cloneRange()
			range.collapse(true)
			let rect = range.getBoundingClientRect()
			if((rect.top === 0 && rect.left === 0) || (rect.width === 0 && rect.height === 0)){
				const editorRect = editorShell.getBoundingClientRect()
				rect = {
					top: editorRect.top + 22,
					left: editorRect.left + 22,
					width: 0,
					height: 0,
					right: editorRect.left + 22,
					bottom: editorRect.top + 22,
					x: editorRect.left + 22,
					y: editorRect.top + 22,
					toJSON: () => ({}),
				} as DOMRect
			}

			this.inlineSuggestionTop = Math.max(rect.top, 20)
			this.inlineSuggestionLeft = Math.max(rect.right + 16, 20)
			this.inlineSuggestionVisible = true
		}

		private scheduleInlineAutocomplete():void{
			if(this.autocompleteTimer){
				clearTimeout(this.autocompleteTimer)
			}

			const sentenceSeed = this.getActiveSentenceSeed()
			if(this.isActive || sentenceSeed.length < 8){
				this.clearInlineSuggestion()
				return
			}

			this.isInlineLoading = true
			this.inlineSuggestion = ''
			this.inlineSuggestionSuffix = ''
			this.emitAutocompleteState([], true)
			this.$nextTick(() => this.updateInlineSuggestionPosition())

			this.autocompleteTimer = setTimeout(() => {
				this.requestInlineAutocomplete(sentenceSeed)
			}, 800)
		}

		private requestInlineAutocomplete(sentenceSeed:string):void{
			const requestId = ++this.autocompleteRequestId
			const form = new FormData()
			form.append('text', sentenceSeed)

			http
				.post('/ai/complete', form)
				.then(response => {
					if(requestId !== this.autocompleteRequestId){
						return
					}
					const suggestions = Array.isArray(response.data) ? response.data.filter((item:string) => !!item) : []
					const topSuggestion = suggestions.length > 0 ? suggestions[0] : ''
					this.inlineSuggestion = topSuggestion
					this.inlineSuggestionSuffix = this.buildSuggestionSuffix(sentenceSeed, topSuggestion)
					this.isInlineLoading = false
					this.emitAutocompleteState(suggestions, false)
					this.$nextTick(() => this.updateInlineSuggestionPosition())
				})
				.catch(() => {
					if(requestId !== this.autocompleteRequestId){
						return
					}
					this.clearInlineSuggestion()
				})
		}

		private isEditorFocused():boolean{
			const activeElement = document.activeElement as HTMLElement | null
			if(!activeElement){
				return false
			}
			return (
				activeElement.classList.contains('ProseMirror') ||
				!!activeElement.closest('.ProseMirror') ||
				(activeElement.getAttribute('contenteditable') === 'true' && !!activeElement.closest('#text-editor')) ||
				!!activeElement.closest('#text-editor [contenteditable="true"]')
			)
		}

		handleEditorKeydown(event: KeyboardEvent):void{
			if(event.key !== 'Tab' || !this.isEditorFocused()){
				return
			}
			event.preventDefault()
			event.stopPropagation()
			if(typeof event.stopImmediatePropagation === 'function'){
				event.stopImmediatePropagation()
			}
			if(this.inlineSuggestionSuffix){
				this.acceptInlineSuggestion()
				return
			}
			document.execCommand('insertText', false, '    ')
		}

		private handleSelectionChange = ():void => {
			if(this.isInlineLoading || this.inlineSuggestionSuffix){
				this.$nextTick(() => this.updateInlineSuggestionPosition())
			}
		}

		private acceptInlineSuggestion():void{
			const activeText = this.getActivePlainText()
			if(activeText.length === 0 || this.inlineSuggestionSuffix.length === 0){
				return
			}

			const separator = /\s$/.test(activeText) ? '' : ' '
			const updatedText = `${activeText}${separator}${this.inlineSuggestionSuffix}`.trim()
			const htmlContent = `<p>${updatedText.replaceAll('\n', '</p><p>')}</p>`

			this.suppressAutocomplete = true
			if(this.activeVal === 1){
				this.itemList[0].text = updatedText
			}else if(this.activeVal > 1){
				for(let i=0; i<this.itemList[0].children.length; i++){
					if(this.activeVal === this.itemList[0].children[i].id){
						this.itemList[0].children[i].text = updatedText
					}
				}
			}

			this.content = htmlContent
			this.setContent(this.content)
			this.updateContent(this.content)
			this.clearInlineSuggestion()
		}

		confirmBack():void{
			if(!confirm('글 저장이 안됐습니다. 이동하시겠습니까?')){
				return
			}else{
				location.href = '/myonego'
			}
		}

		async editTempBoard(tempBoardId:string):Promise<void>{
			//console.log(tempBoardId)
			await http.
				get('/tempBoard',{
					params:{
						'tempBoardId': tempBoardId
					},
					headers:{
						'Authorization': 'Bearer '+localStorage.getItem('accessToken')
					}
				})
				.then(response => {
					//console.log(response.data[0].id)
					this.setId(response.data[0].id)
					this.setMainTitle(response.data[0].title)
					this.setMainSubtitle(response.data[0].subtitle)
					this.setItemList(response.data[0].contents)
					this.setTagList(response.data[0].tags)
					this.setMemoList(response.data[0].memos)
					this.setImageUrl(response.data[0].titleImage)
					//console.log(this.getId)
					eventBus.$emit("clickFirstTree")
				})
				.catch(() => this.errored = true )
				.finally(() => {
					this.loading = false
				})
		}

		async editBoard(boardId:string):Promise<void>{
			//console.log(tempBoardId)
			await http.
				get('/board',{
					params:{
						'boardId': boardId
					},
					headers:{
						'Authorization': 'Bearer '+localStorage.getItem('accessToken')
					}
				})
				.then(response => {
					//console.log(response.data[0].id)
					this.setId(response.data[0].id)
					this.setMainTitle(response.data[0].title)
					this.setMainSubtitle(response.data[0].subtitle)
					this.setItemList(response.data[0].contents)
					this.setTagList(response.data[0].tags)
					this.setMemoList(response.data[0].memos)
					this.setImageUrl(response.data[0].titleImage)
					//console.log(this.getId)
					eventBus.$emit("clickFirstTreePost")
				})
				.catch(() => this.errored = true )
				.finally(() => {
					this.loading = false
				})
		}

		generateSub():void{
			this.isLoading = true

			var subtitle = ''

			var contentList = [] as string[]
			var contents = [] as string[]
			contentList.push(this.itemList[0].text.replaceAll("\n"," ").replaceAll("</p><p>"," ")
									.replaceAll("<strong>","").replaceAll("</strong>","")
									.replaceAll("<em>","").replaceAll("</em>","")
									.replaceAll("<u>","").replaceAll("</u>",""))
			if(this.itemList[0].children.length !== 0){
				for(var i=0; i<this.itemList[0].children.length;i++){
					contentList.push(this.itemList[0].children[i].text.replaceAll("\n"," ").replaceAll("</p><p>"," ")
												.replaceAll("<strong>","").replaceAll("</strong>","")
												.replaceAll("<em>","").replaceAll("</em>","")
												.replaceAll("<u>","").replaceAll("</u>",""))
				}
			}
			contents.push(contentList.join(" "))
			console.log(contents)

			http.
				post('/ai/summarizer',
					{"contents":contents}
				)
				.then(response=>{
					if (response.status >=200 && response.status < 204){
						//console.log(response)
						console.log("success")
						subtitle = response.data
						this.subtitle = subtitle
						this.isLoading = false
					} else{
						//console.log(response)
						console.log("fail..")
					}
				})

			
		}

	}
</script>

<style>
.inline-autocomplete-bubble{
	position:fixed;
	z-index:12;
	padding:8px 12px;
	border-radius:12px;
	background:rgba(255, 255, 255, 0.92);
	border:1px solid rgba(0, 213, 170, 0.18);
	box-shadow:0 10px 24px rgba(0, 0, 0, 0.08);
	backdrop-filter:blur(4px);
	cursor:pointer;
	pointer-events:auto;
	box-sizing:border-box;
	overflow-wrap:anywhere;
	word-break:break-word;
	white-space:normal;
}

.inline-autocomplete-bubble--dark{
	background:rgba(40, 40, 40, 0.94);
	border-color:rgba(0, 213, 170, 0.24);
}

.inline-autocomplete-suggestion{
	display: flex;
	align-items: flex-start;
	gap: 10px;
	color: rgba(70, 70, 70, 0.9);
}
.inline-autocomplete-bubble--dark .inline-autocomplete-suggestion{
	color: rgba(245, 245, 245, 0.92);
}

.inline-autocomplete-label{
	flex: 0 0 auto;
	padding: 2px 8px;
	border-radius: 999px;
	font-size: 0.72rem;
	font-weight: 700;
	letter-spacing: 0.04em;
	color: #00a886;
	background: rgba(0, 213, 170, 0.14);
}

.inline-autocomplete-text{
	position: relative;
	display: inline-block;
	flex: 1 1 auto;
	opacity: 0.82;
	overflow: hidden;
	white-space: normal;
	line-height: 1.5;
}

.inline-autocomplete-text::after{
	content: "";
	position: absolute;
	inset: 0;
	transform: translateX(-120%);
	background: linear-gradient(90deg, transparent, rgba(255,255,255,0.75), transparent);
	animation: inline-autocomplete-shimmer 2.2s infinite;
	pointer-events: none;
}

.inline-autocomplete-hint{
	font-size: 0.9rem;
	color: rgba(90, 90, 90, 0.78);
}

.inline-autocomplete-bubble--dark .inline-autocomplete-hint{
	color: rgba(240, 240, 240, 0.72);
}

@keyframes inline-autocomplete-shimmer{
	100%{
		transform: translateX(120%);
	}
}
</style>
