<!--suppress CssUnusedSymbol -->
<template>
  <div>
    <Slide id="slide-menu" :closeOnNavigation="true">
      <h1>BELAZZZ NOTEBOOK</h1>
      <router-link to="/tasks">Задания</router-link>
      <router-link to="/clients">Список клиентов</router-link>
      <button id="export-btn" class="btn">Экспорт данных</button>
    </Slide>
  </div>
</template>

<script>
import { Slide } from "vue3-burger-menu";
export default {
  name: "burger-menu",
  components: {
    Slide,
  },
};
</script>

<style>
/*router-link style*/
a {
  background-color: #00abc3;
  color: #f6f9e5;
  padding: 12px 8px;
  box-shadow: 1px 2px 4px #2d2d2d;
  margin: 10px 0;
}
.bm-burger-button {
  top: 1.15rem;
  left: 1rem;
  width: 20px;
  height: 15px;
  cursor: pointer;
}
.bm-burger-bars {
  background-color: #00abc3;
}
.bm-menu {
  background-image: linear-gradient(315deg, #05668d 0%, #00a896 65%);
}
.bm-item-list {
  margin: auto;
}
nav a.router-link-exact-active {
  color: #000;
  background: #f0f3bd;
}
nav h1 {
  color: #f6f9e5;
  margin: 5px 0;
}
#export-btn {
  position: absolute;
  bottom: 2rem;
  left: 8rem;
}
</style>