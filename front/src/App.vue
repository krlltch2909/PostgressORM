<!--suppress ALL -->
<template>
  <router-view/>
</template>

<script>


import MainPage from "@/views/MainPage";
export default {
  name: 'App',
  components: {MainPage},
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
.app{
  margin: 50px;
}
</style>
