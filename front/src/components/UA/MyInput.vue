<template>
  <input class="input" :value="modelValue" @input="getInput" type="text">
</template>

<script>
export default {
  name: "my-input",
  props:{
    modelValue: [String, Number]
  },
  methods: {
    getInput(event){
      this.$emit('update:modelValue', event.target.value)
    }
  },
}
</script>

<style scoped>
.input{
  width: 100%;
  border: 1px solid teal;
  padding: 15px;
  margin-top: 15px;
}
</style>