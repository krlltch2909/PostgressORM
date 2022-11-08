<template>
  <div>
    <form>
      <h3>creation new user</h3>
      <my-input
          v-model.trim="user.login"
          placeholder="login"/>
      <my-input
          v-model.trim="user.password"
          placeholder="password"/>
      <my-input
          v-model.trim="user.user_name"
          placeholder="name"/>

      <my-select :options="roles" v-model="selectedRole"/>

      <button type="button" @click="createNewPost" class="btn btn-success">create</button>
    </form>
  </div>
</template>

<script>
import MySelect from "@/components/UA/MySelect";
export default {
  name: "my-create-user",
  components: {MySelect},
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