<template>
  <div>
    <h3>Редактирование задачи</h3>

    <div v-if="error !== ''">
      <div class="alert alert-danger" role="alert">
        {{ error }}
      </div>
    </div>

    <div class="select-name">
      <b>Дата исполнения</b>
      <input id="date" type="date"
             class="date__input"
             v-model="task.term_of_execution">
    </div>


    <div class="select-name">
      <h6>Тип задачи</h6>
      <base-select
          :options="all_task_type_codes"
          v-model="task.task_type_code"
          :model-value="task.task_type_code"/>
    </div>


    <div class="select-name">
      <h6>Приоритет</h6>
      <base-select
          :options="all_priority_codes"
          v-model="task.priority_code"
      :model-value="task.priority_code"/>
    </div>


    <div v-if="role !== 'worker'" class="select-name">
      <h6>Исполнитель</h6>
      <base-select :options="all_employees" v-model="task.performer_number" :model-value="task.performer_number"/>
    </div>


    <button id="create__contract__btn" type="button" @click="editTask" class="btn">Применить</button>
  </div>
</template>

<script>
import BaseSelect from "@/components/BaseSelect";
import axios from "axios";

export default {
  name: "task-edit-popup",
  components: {BaseSelect},
  props: {
    all_task_type_codes: {
      type: Array
    },
    all_priority_codes: {
      type: Array
    },
    role: {
      type: String
    },
    all_employees: {
      type: Array
    },
    task: {
      type: Object
    }
  },
  computed: {
    getConfig() {
      return this.$store.getters.getConfig;
    },
  },

  data() {
    return {
      input_date: this.task.term_of_execution,
      selectedTypeCode: this.task.task_type_code,
      selectedPriorityCode: this.task.priority_code,
      performer_login: this.task.performer_number,
      error: '',
    }
  },
  methods: {
    // Эта хренотень до сих пор не работает, потому что Кирюха не сделал нормальный API
    async editTask() {
      this.$emit('editTask', this.task)

      const url_for_task_edit = process.env.VUE_APP_API + '/tasks/'

      let taskFormData = new FormData();

      console.log(this.task)

      taskFormData.append('id', this.task.id)
      taskFormData.append('term_of_execution', this.task.term_of_execution);
      taskFormData.append('contract_number', this.task.contract_number);
      taskFormData.append('priority_code', this.task.priority_code);
      taskFormData.append('task_type_code', this.task.task_type_code);
      taskFormData.append('performer_number', this.task.performer_id);
      taskFormData.append('status', this.task.status);


      await axios.put(url_for_task_edit, taskFormData, this.getConfig)
        .then(response => {
          console.log(response)
          this.$emit('close')
        })
        .catch(error => {
          console.log(error)
          this.error = error.response.data
        })
    }
  }
}
</script>

<style scoped>
.create-contract {
  display: flex;
  align-items: center;
  margin: 10px;
}

.date-input {
  border: 1px solid black;
  width: 100%;
  border-radius: 5px;
}

.select-name {
  display: flex;
  margin: 5px;
  width: 100%;
}

</style>