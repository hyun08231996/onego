<template>
  <div class="align-center member-card">
    <v-container>

      <v-row no-gutters  id="memberCard">
        <!-- col 1 -->
        <v-col>
          <v-card :loading="loading" class="mx-auto my-12" max-width="374">
            <template slot="progress">
              <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
            </template>

            <v-avatar>
              <img
                src="@/assets/profile/dogKang.jpeg"
                alt="강지원"
              >
            </v-avatar>
            <v-card-title>강지원</v-card-title>

            <v-card-text>
              <div class="my-4 text-subtitle-1">
                AI Developer
              </div>

              <div>When you're feeling a bit <br>out of sorts, don't worry!<br>You're probably just hungry</div>
            </v-card-text>

            <v-divider class="mx-4"></v-divider>
          </v-card>
          <v-card :loading="loading" class="mx-auto my-12" max-width="374">
            <template slot="progress">
              <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
            </template>

            <v-avatar>
              <img
                src="@/assets/profile/sangsoon.jpg"
                alt="이상순"
              >
            </v-avatar>
            <v-card-title text-align="center">이상순</v-card-title>

            <v-card-text>

              <div class="my-4 text-subtitle-1">
                DEVOPS
              </div>

              <div>I want to make the world <br>more convenient.</div>
            </v-card-text>

            <v-divider class="mx-4"></v-divider>
          </v-card>
        </v-col>
        <!-- col 2 -->
        <v-col>
          <v-card :loading="loading" class="mx-auto my-12" max-width="374">
            <template slot="progress">
              <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
            </template>

            <v-avatar>
              <img
                src="@/assets/profile/yeram.jpg"
                alt="권예람"
              >
            </v-avatar>
            <v-card-title text-align="center">권예람</v-card-title>

            <v-card-text>

              <div class="my-4 text-subtitle-1">
                FE Developer
              </div>

              <div>새로운 도전을 하는걸 <br>좋아합니다</div>
            </v-card-text>

            <v-divider class="mx-4"></v-divider>
          </v-card>
          <v-card :loading="loading" class="mx-auto my-12" max-width="374">
            <template slot="progress">
              <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
            </template>

            <v-avatar>
              <img
                src="@/assets/profile/sooyoung.jpg"
                alt="이수영"
              >
            </v-avatar>
            <v-card-title text-align="center">이수영</v-card-title>

            <v-card-text>

              <div class="my-4 text-subtitle-1">
                FE Developer
              </div>

              <div>It's not a problem, <br> it's just a challenge</div>
            </v-card-text>

            <v-divider class="mx-4"></v-divider>
          </v-card>

        </v-col>
        <!-- col 3 -->
        <v-col>
          <v-card :loading="loading" class="mx-auto my-12" max-width="374">
            <template slot="progress">
              <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
            </template>

            <v-avatar>
              <img
                src="@/assets/profile/peter.jpg"
                alt="남승현"
              >
            </v-avatar>
            <v-card-title text-align="center">남승현</v-card-title>

            <v-card-text>

              <div class="my-4 text-subtitle-1">
                FE Developer
              </div>

              <div>Never give up because <br>great things take time.</div>
            </v-card-text>

            <v-divider class="mx-4"></v-divider>
          </v-card>
          <v-card :loading="loading" class="mx-auto my-12" max-width="374">
            <template slot="progress">
              <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
            </template>

            <v-avatar>
              <img
                src="@/assets/profile/jaeho.jpg"
                alt="이재호"
              >
            </v-avatar>
            <v-card-title text-align="center">이재호</v-card-title>

            <v-card-text>

              <div class="my-4 text-subtitle-1">
                BE Developer
              </div>

              <div>실험이 많을수록, <br>더 좋은 결과를 이끌어낸다.</div>
            </v-card-text>

            <v-divider class="mx-4"></v-divider>
          </v-card>

        </v-col>
        <!-- col 4 -->
        <v-col>
          <v-card :loading="loading" class="mx-auto my-12" max-width="374">
            <template slot="progress">
              <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
            </template>

            <v-avatar>
              <img
                src="@/assets/profile/youngsu.jpeg"
                alt="오영수"
              >
            </v-avatar>
            <v-card-title text-align="center">오영수</v-card-title>

            <v-card-text>

              <div class="my-4 text-subtitle-1">
                AI Developer
              </div>

              <div>With hard work and effort, <br>you can achieve anything.</div>
            </v-card-text>

            <v-divider class="mx-4"></v-divider>
          </v-card>
          <v-card :loading="loading" class="mx-auto my-12" max-width="374">
            <template slot="progress">
              <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
            </template>

            <v-avatar>
              <img
                src="@/assets/profile/catlim.jpg"
                alt="임세홍"
              >
            </v-avatar>
            <v-card-title text-align="center">임세홍</v-card-title>

            <v-card-text>

              <div class="my-4 text-subtitle-1">
                BE Developer
              </div>

              <div>판.교.좋.아.</div>
            </v-card-text>

            <v-divider class="mx-4"></v-divider>
          </v-card>

        </v-col>
      </v-row>

    </v-container>


  </div>
</template>
<script>
  export default {
    data: () => ({
      loading: false,
      selection: 1,
    }),

    methods: {
      reserve () {
        this.loading = true

        setTimeout(() => (this.loading = false), 2000)
      },
    },
  }
</script>
<style>
  .member-card .v-card{
    width: 270px;
  }
  .v-application .my-4 {
     margin-top: 0px !important;
  }
  .v-avatar{
    margin-top: 50px;
    height: 90px !important;
    min-width: 90px !important;
    width: 90px !important;
  }
  .v-card__title {
        display: block;
  }
  /* .v-card__text{
    text-align: center
  } */
  .align-center{
    /* align-items: center; */
    text-align: center
  }

  #memberCard .v-card__text{
    height: 140px;
  }
</style>