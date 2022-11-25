<template>
  <div class="layout">
    <navbar/>
      <main class="layout-content">
        <router-view/>
      </main>
  </div>
</template>

<script>
export default {
  name: "Layout"
}
</script>

<style>
.layout-content {
  margin: 1rem;
}
h2{
  color: #05668d;
}
.btn {
  margin-left: auto;
  display: flex;
  background-color: #00abc3;
  border: none;
  border-radius: 5px;
  color: #fff;
}
.btn:hover {
  background-color: #00a896;
  border: none;
}
</style>