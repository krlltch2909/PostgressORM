<!--suppress CssUnusedSymbol -->
<!-- Надо будет придумать как переименовать сам файл, чтобы он подходил под общую структуру -->
<template>
  <div>
      <Slide id="Slide">
        <h1>BELAZZZ NOTEBOOK</h1>
        <router-link to="/tasks">Задания</router-link>
        <router-link to="/clients">Список клиентов</router-link>
      </Slide>
    <router-view />
  </div>
</template>

<script>
import { Slide } from "vue3-burger-menu";
export default {
  name: "burger-menu",
  components: {
    Slide,
  }
};
</script>

<style>
.bm-burger-button {
  top: 18px;
  left: 15px;
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
nav router-link {
  color: #f6f9e5;
  padding: 11.5px 7.5px;
  box-shadow: 1px 2px 4px #2d2d2d;
  margin: 10px 0;
}
nav a.router-link-exact-active {
  color: #000;
  background: #f0f3bd;
}
nav h1 {
  color: #f6f9e5;
  margin: 10px 0;
}
</style>