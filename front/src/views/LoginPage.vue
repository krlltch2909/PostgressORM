<template>
  <h2 id="auth-text">Авторизуйтесь в системе для доступа к заданиям</h2>
  <div class="login">
    <div class="input-auth">
      <base-input v-model="username"
                  placeholder="Логин"/>
      <!--
       Не совсем понимаю зачем делать отдельный input, если можно использовать обычный со стилем
       Но ладно, хрен с тобой
       -->
      <base-input v-model="password"
                  placeholder="Пароль" type="password"/>
    </div>
    <div>
      <button id="enter" type="button" @click="getTasks"
              class="btn">Войти</button>
    </div>
  </div>
</template>

<script>

import axios from "axios";
import BaseInput from "@/components/BaseInput";
import router from "@/router";
import store from "@/store";


export default {
  name: "login-page",
  components: {
    BaseInput,
  },
  computed:{
    getConfig(){
      return store.getters.getConfig;
    }
  },

  data(){
    return{
      username: 'nick',
      password: 'qwerty',
    }
  },
  methods: {
    async getTasks() {
      try {
        const response = await axios.get(process.env.VUE_APP_API + '/tasks/?username=' + this.username + '&password=' + this.password, this.getConfig);
        localStorage.setItem('username', this.username)
        localStorage.setItem('password', this.password)
        const roleResponse = await axios.get(process.env.VUE_APP_API + '/users/?login=' + localStorage.getItem('username'), this.getConfig)
        this.$store.commit('setRole', roleResponse.data['iAm']['role'])
        this.$store.commit('setLoggedIn', true)
        await router.push({name: 'tasks'})

      } catch (e) {
        alert('Неверный логин или пароль')
      }
    }
  }
}
</script>

<style>
#auth-text{
  text-align: center;
  margin-top: 4rem;
}
.login{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 4rem;
}
#enter{
  margin-top: 1rem;
}
</style>