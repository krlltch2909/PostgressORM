<template>
  <div>
    <h3>Create new Task</h3>
    <my-input
        v-model.trim="task.term_of_execution"
        placeholder="term of execution"/>
    <my-select :options="all_task_type_codes" v-model="selectedTypeCode"/>
    <my-select :options="all_priority_codes" v-model="selectedPriorityCode"/>

    <div class="create__contract">
      <h8>Create New Contract</h8>
      <input class="form-check-input mt-0"
             v-model="createNewContract" type="checkbox" value=""
             style="margin-left: auto"
             aria-label="Checkbox for following text input">
    </div>

    <div class="contract" v-if="createNewContract === true">
      <my-input
          v-model.trim="contract.contract_details"
          placeholder="contract details"/>
      <my-input
          v-model.trim="contract.vin"
          placeholder="vin"/>
      <my-input
          v-model.trim="contract.license_plate"
          placeholder="license plate"/>
    </div>


    <button type="button" @click="createNewTask" class="btn btn-success">create</button>
  </div>
</template>

<script>
import MySelect from "@/components/UA/MySelect";
export default {
  name: "my-create-task",
  components: {MySelect},
  props:{
    all_task_type_codes:{
      type: Array
    },
    all_priority_codes:{
      type: Array
    }
  },

  data() {
    return{
      createNewContract: false,
      selectedTypeCode: String,
      selectedPriorityCode: String,
      task: {
        term_of_execution: '',
        contract_number: null,
        author_number: 1,
        priority_code: '',
        task_type_code: ''
      },
      contract: {
        contract_details: '',
        vin: '',
        license_plate: ''
      }
    }
  },
  methods:{
    createNewTask(){


      if (this.selectedPriorityCode === ''){
        alert("task priority must be chosen")
        return
      }

      if (this.selectedTypeCode === ''){
        alert("task type code must be chosen")
        return
      }

      if (this.createNewContract === true){
        if (this.contract.vin.length > 9){
          alert("vin must be no more then 9")
          return
        }
      }

      this.task.task_type_code = this.all_task_type_codes.find(el => el.value === this.selectedTypeCode)['id']
      this.task.priority_code = this.all_priority_codes.find(el => el.value === this.selectedPriorityCode)['id']
      if (this.createNewContract === true){
        this.task.contract_number = this.contract
      }


      this.$emit('createTask', this.task)
      this.task = {
        term_of_execution: '',
        contract_number: '',
        priority_code: '',
        task_type_code: ''
      }
      this.contract =  {
        contract_details: '',
        vin: '',
        license_plate: ''
      }

    }
  }
}
</script>

<style scoped>
.create__contract{
  display: flex;
  align-items: center;
  margin: 10px;
}
</style>