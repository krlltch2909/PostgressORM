<template>
  <my-main-page/>
</template>

<script>


import MyMainPage from "@/components/MainPage";
export default {
  name: 'App',
  components: {MyMainPage},
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
