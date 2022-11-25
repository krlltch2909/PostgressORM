<template>
  <div class="client">
    <div v-for="(values, client_id) in clients" :key="client_id" >
      <strong>{{client_id}}: </strong>{{values}}
    </div>
  </div>
</template>

<script>
export default {
  name: "client-item",
  props:{
    clients: {
      type: Object,
      require: true
    }
  }
}
</script>

<style>
.client {
  padding: 20px;
  border: 2px solid #00abc3;
  border-radius: 10px;
  margin: 15px;
  align-items: center;
}

</style>