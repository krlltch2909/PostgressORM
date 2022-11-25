<template>
  <div>
    <h3>Создание задачи</h3>

    <div v-if="error !== ''">
      <div class="alert alert-danger" role="alert">
        {{error}}
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
          v-model="selectedTypeCode"/>
    </div>


    <div class="select-name">
      <h6>Приоритет</h6>
      <base-select
          :options="all_priority_codes"
          v-model="selectedPriorityCode"/>
    </div>


    <div  v-if="role !== 'worker'" class="select-name">
      <h6>Исполнитель</h6>
      <base-select :options="all_employees" v-model="performer_login"/>
    </div>

    <div class="create-contract">
      <b>Внести новый контракт</b>
      <input class="form-check-input mt-0"
             v-model="createNewContract" type="checkbox"
             style="margin-left: auto"
             aria-label="Checkbox for following text input">
    </div>

    <div class="contract" v-if="createNewContract === true">
      <base-input
          v-model.trim="contract.contract_details"
          placeholder="contract details"/>
      <base-input
          v-model.trim="contract.vin"
          placeholder="vin"/>
      <base-input
          v-model.trim="contract.license_plate"
          placeholder="license plate"/>
    </div>


    <button id="create__contract__btn" type="button" @click="createNewTask" class="btn">Создать</button>
  </div>
</template>

<script>
import BaseSelect from "@/components/BaseSelect";
import Datepicker from '@vuepic/vue-datepicker';

export default {
  name: "task-create-popup",
  components: {BaseSelect, Datepicker},
  props:{
    all_task_type_codes:{
      type: Array
    },
    all_priority_codes:{
      type: Array
    },
    role:{
      type: String
    },
    all_employees:{
      type: Array
    }
  },

  data() {
    return{
      // input_date: Date,
      createNewContract: false,
      selectedTypeCode: '',
      selectedPriorityCode: '',
      performer_login: '',
      error: '',
      task: {
        term_of_execution: '',
        contract_number: null,
        author_number: 1,
        priority_code: '',
        task_type_code: '',
        performer_id: '',
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

      if (this.task.term_of_execution === ''){
        this.error= "Необходимо указать дату исполнения"
        return
      }
      else {
        this.error = ''
      }

      if (this.selectedPriorityCode === ''){
        this.error= "Необходимо указать приоритет"
        return
      }

      if (this.selectedTypeCode === ''){
        alert("Необходимо указать тип задачи")
        return
      }

      if (this.createNewContract === true){
        if (this.contract.vin.length > 9){
          alert("VIN не может быть длиннее 9 символов")
          return
        }
      }


      this.task.task_type_code = this.all_task_type_codes.find(el => el.value === this.selectedTypeCode)['id']
      this.task.priority_code = this.all_priority_codes.find(el => el.value === this.selectedPriorityCode)['id']

      if (this.createNewContract === true){
        this.task.contract_number = this.contract
      }

      try{
        this.task.performer_id = this.all_employees.find(el => el.value === this.performer_login)['id']
      }
      catch (e){
        this.task.performer_id = ''
      }




      this.$emit('createTask', this.task)
      this.task = {
        term_of_execution: '',
        contract_number: '',
        priority_code: '',
        task_type_code: '',
        performer_login: ''
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
.create-contract{
  display: flex;
  align-items: center;
  margin: 10px;
}
.date-input{
  border: 1px solid black;
  width: 100%;
  border-radius: 5px;
}
.select-name{
  display: flex;
  margin: 5px;
  width: 100%;
}

</style>