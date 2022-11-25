<template>
  <div class="task">
    <div>
    <!-- TODO: Попробовать перевести эту хрень. Но тут всё придётся менять -->
      <div v-for="(values, key_task) in task" :key="key_task">
        <div v-if="key_task !== 'contact_number'">
          <strong>{{key_task}}: </strong>{{values}}
        </div>

        <div v-else-if="values !== null" class="v_else">
          <strong>{{key_task}}:</strong>
          <contract-item :contract="values"/>
        </div>
        
      </div>
    </div>

    <button id="edit-task-btn"
            type="button"
            @click="$emit('show_task_changer', task)"
            class="btn">Редактировать</button>
  </div>
</template>

<script>

import ContractItem from "@/components/ContractItem";
export default {
  name: 'task-item',
  components: {ContractItem},
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
  border: 2px solid #00abc3;
  border-radius: 10px;
  margin-top: 1rem;
  display: flex;
  align-items: center;
}
#edit-task-btn{
  margin-left: auto;
}
.v_else{
  display: flex;
  margin: 5px;
  align-items: center;
}
</style>