<template>
  <div class="task">
    <div>
      <div v-for="(values, key_task) in task" :key="key_task">
        <div v-if="key_task !== 'contact_number'">
          <strong>{{key_task}}: </strong>{{values}}
        </div>

        <div v-else-if="values !== null" class="v_else">
          <strong>{{key_task}}:</strong>
          <my-contract-item :contract="values"/>
        </div>

      </div>
    </div>

    <div class="task__button">
      <button type="button" class="btn btn-danger"
              @click="$emit('show_task_changer', task)"
      >Edit</button>
    </div>

  </div>

</template>

<script>

import MyContractItem from "@/components/UA/ContractItem";
export default {
  name: 'my-task-item',
  components: {MyContractItem},
  props: {
    task: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.task {
  padding: 20px;
  border: 2px solid teal;
  margin: 15px;
  display: flex;
  align-items: center;
}
.task__button{
  padding: 20px;
  margin-left: auto;
}
.v_else{
  display: flex;
  margin: 5px;
  align-items: center;
}
</style>