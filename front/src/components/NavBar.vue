<template>
  <header id="navbar">
    <burger-menu v-if="loggedIn"/>
    <div class="app-name"><strong>BELAZZZ NOTEBOOK</strong></div>
    <div class="navbar-buttons" v-if="loggedIn">
      <button
          id="create-user-btn"
          type="button"
          class="btn"
          v-if="dbRole === 'administrator'"
          style="margin-left: 20px"
          @click="addUserDialog">Создать пользователя</button>

      <button
          id="change-user-btn"
          type="button"
          class="btn"
          @click="changeUser">Выйти</button>
    </div>
  </header>
  <base-dialog v-model:show="add_dialog_visible">
    <user-create-popup :roles="allDbRoles" @createUser="createUser"/>
  </base-dialog>
</template>

<script>

import BurgerMenu from "@/components/BurgerMenu";
import axios from "axios";
import router from "@/router";
import UserCreatePopup from "@/components/UserCreatePopup";
import BaseDialog from "@/components/BaseDialog";

export default {
  name: "navbar",
  components: {
    "burger-menu": BurgerMenu,
    "user-create-popup": UserCreatePopup,
    "base-dialog": BaseDialog
  },
  computed: {
    loggedIn(){
      return this.$store.state.loggedIn
    }
  },

  data(){
    return{
      // Ну так-то это в бэкенде должно быть
      allDbRoles: [
        {id: 1, value:'worker'},
        {id: 2, value:'manager'},
        {id: 3, value:'administrator'},
      ],

      add_dialog_visible: false,
    }
  },

  methods: {
    async changeUser() {
      this.username = ''
      this.password = ''
      this.dbRole = ''
      this.tasks = []
      this.$store.commit('setLoggedIn', false)

      await router.push({name: 'login'})
    },

    addUserDialog() {
      this.add_dialog_visible = true
    },

    // создание нового пользователя
    async createUser(user) {
      try {

        const url = process.env.VUE_APP_API + '/users/?username=' + this.username + '&password=' + this.password

        let formData = new FormData();

        formData.append('login', user['login']);
        formData.append('password', user['password']);
        formData.append('name', user['user_name']);
        formData.append('role', user['role']);


        const response = await axios.post(url, formData, this.config)


        if (response.data === 200){
          alert(e)
        }
        else {
          this.add_dialog_visible = false
        }

      } catch (e) {
        alert(e)
      }
    },
  }
}
</script>

<style scoped>
header {
  height: 50px;
  background-color: #05668d;
  box-shadow: 2px 2px 4px gray;
  display: flex;
  align-items: center;
  padding: 20px;
}
.navbar-buttons {
  margin-left: auto;
}
.app-name{
  margin-left: 30px;
  color: #f6f9e5;
}

</style>