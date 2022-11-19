<template>
  <div>
    <form>
      <h3>Создание нового пользователя</h3>
      <base-input
          v-model.trim="user.login"
          placeholder="login"/>
      <base-input
          v-model.trim="user.password"
          placeholder="password"/>
      <base-input
          v-model.trim="user.user_name"
          placeholder="name"/>

      <base-select :options="roles" v-model="selectedRole"/>

      <button type="button" @click="createNewPost" class="btn btn-success">create</button>
    </form>
  </div>
</template>

<script>
import BaseInput from "@/components/BaseInput";
import BaseSelect from "@/components/BaseSelect";
export default {
  name: "user-create-popup",
  components: {BaseSelect, BaseInput},
  props:{
    selectedRole: String,
    roles: {
      type: Array,
    }
  },

  data() {
    return{
      user: {
        login: '',
        password: '',
        user_name: '',
        role: ''
      }
    }
  },
  methods: {
    createNewPost(){
      this.user.id = Date.now()
      this.user.role = this.selectedRole
      console.log(this.user)

      this.$emit('createUser', this.user)
      this.user = {
        login: '',
        password: '',
        user_name: ''
      }
    },
  }
}
</script>

<style scoped>


.btn {
  margin-top: 15px;
  align-self: flex-end;
}
form{
  display: flex;
  flex-direction: column;
}

</style>