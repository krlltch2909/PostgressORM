<template>
  <div class="navBar">
    <BurgerMenu/>
    <div class="app__name"><strong>BELAZZZ NOTEBOOK</strong></div>
    <div class="naveBar__buttons">
      <slot>
      </slot>
    </div>
  </div>
</template>

<script>
import BurgerMenu from "@/components/BurgerMenu";
export default {
  name: "navbar",
  components: {
    BurgerMenu,
  },
}
</script>

<style scoped>
.navBar{
  height: 50px;
  background-color: #05668d;
  box-shadow: 2px 2px 4px gray;
  display: flex;
  align-items: center;
  padding: 20px;
}
/* ??????? */
.naveBar__buttons{
  margin-left: auto;
}
.app__name{
  margin-left: 30px;
  color: #f6f9e5;
}

</style>