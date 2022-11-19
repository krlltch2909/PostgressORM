<template>
  <nav-bar :login="isLogin"/>
  <div class="login">
    <div class="input__auth">
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
      <button type="button" @click="getTasks"
              class="btn btn-success">Войти</button>
    </div>
  </div>
</template>

<script>

import axios from "axios";
import BaseInput from "@/components/BaseInput";
import NavBar from "@/components/NavBar";
import router from "@/router";


export default {
  name: "main-page",
  components: {
    BaseInput,
    NavBar
  },


  data(){
    return{
      username: 'nick',
      password: 'qwerty',

      isLogin: false,

      config: {
        headers:{
          // ХАРДКОД (╯°□°）╯︵ ┻━┻
          'Authorization': 'Token e222cdf2fae4ff2e6494640269f150b4ff52f468'
        }
      }
    }
  },
  methods: {
    async getTasks() {
      try {
        const response = await axios.get(process.env.VUE_APP_API + '/tasks/?username=' + this.username + '&password=' + this.password, this.config)
        this.isLogin = true
        await router.push({name: 'tasks'})

      } catch (e) {
        alert('Неверный логин или пароль')
      }
    }
  }
}
</script>

<style>
.input__auth{
  margin-left: 5px;
}
</style>