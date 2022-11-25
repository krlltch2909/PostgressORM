<template>
  <div class="contract">
    <div v-for="(values, key_task) in contract" :key="key_task" >
      <div v-if="key_task !== 'contact_number'">
        <strong>{{key_task}}: </strong>{{values}}
      </div>
    </div>
  </div>

</template>

<script>
export default {
  name: "contract-item",
  props:{
    contract: {
      require: true
    }
  }
}
</script>

<style scoped>
.contract {
  padding: 20px;
  border: 2px solid #00abc3;
  border-radius: 10px;
  margin: 15px;
  align-items: center;
}
</style>