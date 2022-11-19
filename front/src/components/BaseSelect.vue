<template>
  <select style="margin-top: 10px" v-model="modelValue" @input="changeOption" class="form-select" aria-label="Default select example">
    <option disabled value="">Выбрать из списка</option>
    <option
        v-for="element in options"
        :key="element.id"
        :value="element.value"
    >
      {{element.value}}
    </option>
  </select>

</template>

<script>
export default {
  name: "base-select",
  props:{
    modelValue: String,
    options: {
      type: Array,
      default: () => [],
    },
  },

  methods:{
    changeOption(event){

      this.$emit('update:modelValue', event.target.value)
    },
  }
}
</script>

<style scoped>

</style>