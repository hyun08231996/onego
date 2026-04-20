import Vue from 'vue'
import Vuex, {StoreOptions} from 'vuex'
import authStore from '@/store/modules/authStore'
import writeStore from '@/store/modules/writeStore'
import { Auth } from 'aws-amplify'

Vue.use(Vuex)

export interface RootState {
	user:{
		signedIn: boolean,
		userAccount: any,
		userInfo: any
	};
	accessToken:string;
	followerUser:string;
	followingUser:string;
}

const index: StoreOptions<RootState> = {
  modules: {
    authStore:authStore,
	writeStore:writeStore,
  },
  state: {
    user: {
      signedIn: false,
      userAccount: new Object(),
      userInfo: new Object()
    },
    accessToken: '',
    followerUser: '',
    followingUser: ''
  },
  mutations: {
    changeSignedInState: function(state, user){
      Vue.set(state.user, 'signedIn', !!user)
      Vue.set(state.user, 'userAccount', user)
    },
    setAccessToken: function(state, token){
      Vue.set(state, 'accessToken', token)
    },
    setUserInfo: function(state, user){
      Vue.set(state.user, 'userInfo', user)
    },
    setFollowerUser: function(state, user){
      Vue.set(state, 'followerUser', user)
    },
    setFollowingUser: function(state, user){
      Vue.set(state, 'followingUser', user)
    }

  },
  getters: {
    getSignedIn: function(state){
      return state.user.signedIn
    }
  },
  actions: {
    findUser: async function({ commit }){
      try {
        const user = await Auth.currentAuthenticatedUser();
        commit('changeSignedInState', user);

        const result: any = await Auth.currentSession();
        commit('setAccessToken', result.accessToken.jwtToken);
        localStorage.setItem('accessToken', result.accessToken.jwtToken);

        const storedUserInfo = localStorage.getItem('userInfo');
        if (storedUserInfo) {
          commit('setUserInfo', JSON.parse(storedUserInfo));
        }
      } catch (error) {
        console.log('not signed in', error);
        commit('changeSignedInState', null);
        commit('setAccessToken', '');
      }
    },
    // setU
  },
}

export default new Vuex.Store(index)
