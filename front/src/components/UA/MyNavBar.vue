<template>
  <div class="navBar">
    <div class="app__name"><strong>BELAZZZ NOTEBOOK</strong></div>
    <div class="naveBar__buttons">
      <slot>

      </slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "my-nav-bar"
}
</script>

<style scoped>
.navBar{
  height: 50px;
  background-color: teal;
  box-shadow: 2px 2px 4px gray;
  display: flex;
  align-items: center;
  padding: 15px;
}
.naveBar__buttons{
  margin-left: auto;
}
.app__name{
  color: darkorange;
}

</style>