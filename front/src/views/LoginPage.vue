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
      <button id="enter" type="button" @click="logIn"
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
  computed: {
    getConfig() {
      return store.getters.getConfig;
    }
  },

  data() {
    return {
      username: 'nick',
      password: 'qwerty',
    }
  },
  methods: {
    async logIn() {
      try {
        const response = await axios.post(process.env.VUE_APP_API + '/auth/', {
          login: this.username,
          password: this.password
        }, this.getConfig);
        if (response.status !== 200) return alert('Неверный логин или пароль');

        // По-хорошему надо бы сделать нормальное сохранение куки, мб через vue-cookies
        // Но у меня не получалось его настроить, поэтому пока так

        // this.$cookies.set('token', response.data.token, '1D', '/', '', false, 'Strict');
        // console.log(this.$cookies)

        // Поставить куки мы поставили, теперь их надо как-то передавать. Так что пока это TODO.
        document.cookie = `token=${response.data.token}; path=/; expires=${new Date(Date.now() + 86400e3).toUTCString()};`;

        // localStorage.setItem('session', response.data.token);
        const roleResponse = await axios.get(process.env.VUE_APP_API + '/users/', this.getConfig)
        this.$store.commit('setRole', roleResponse.data['iAm']['role'])
        this.$store.commit('setLoggedIn', true)
        await router.push({name: 'tasks'})
      } catch (e) {
        console.log(e);
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