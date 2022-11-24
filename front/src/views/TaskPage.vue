<template>
  <main class="layout-content">
    <div class="task-headers">
      <h2>Список задач</h2>
      <div class="task-buttons">
        <button id="export-btn"
                style="margin-right: 1rem"
                @click="exportTasks"
                class="btn">Экспорт данных</button>
        <button id="add-task"
                @click="add_task_dialog_visible = true"
                class="btn">Создать задачу</button>
      </div>
    </div>
    <task-list :tasks="tasks"
               @create_task="createTaskDialog"
    />
  </main>
    <base-dialog v-model:show="add_task_dialog_visible">
      <task-create-popup :all_priority_codes="priority_codes"
                         :all_task_type_codes="tasks_type_classifier"
                         :all_employees="employees"
                         :role="dbRole"
                         @createTask="createTask"
      />
    </base-dialog>

</template>

<script>

import axios from "axios";
import TaskList from "@/components/TaskList";
import BaseInput from "@/components/BaseInput";
import UserCreatePopup from "@/components/UserCreatePopup";
import TaskCreatePopup from "@/components/TaskCreatePopup";
import router from "@/router";
import store from "@/store";


// IDE-шка врёт, что beforeMount не используется и меня это бесит
// noinspection JSUnusedGlobalSymbols
export default {
  name: "task-page",
  components: {
    TaskCreatePopup,
    UserCreatePopup,
    BaseInput,
    TaskList
  },
  computed:{
    getConfig(){
      return store.getters.getConfig;
    },
    dbRole(){
      return store.getters.getRole;
    },
  },


  data(){
    return{
      tasks: [],
      tasks_type_classifier: [],
      contracts: [],
      employees: [],
      priority_codes: [],
      // видимость диалогов
      add_task_dialog_visible: false,

      // для выпадающих списков
      priorityCodeSort: ''
    }
  },


  methods:{
    createTaskDialog(){
      this.add_task_dialog_visible = true
    },

    // создание нового задания
    async createTask(task){

      try {
        if (task.contract_number !== null) {
          const contract_url = process.env.VUE_APP_API + '/contracts/?username=' +
              localStorage.getItem('username') + '&password=' + localStorage.getItem('password')
          let formData = new FormData();

          formData.append('contract_details', task.contract_number.contract_details);
          formData.append('vin', task.contract_number.vin);
          formData.append('license_plate', task.contract_number.license_plate);


          const response = await axios.post(contract_url, formData, this.getConfig)

          task.contract_number = response.data['id'][0][0]
        }

        const url_for_task_add = process.env.VUE_APP_API + '/tasks/?username='
            + localStorage.getItem('username') + '&password=' + localStorage.getItem('password')

        console.log(task)

        let taskFormData = new FormData();

        taskFormData.append('term_of_execution', task.term_of_execution);
        taskFormData.append('contract_number', task.contract_number);
        taskFormData.append('priority_code', task.priority_code);
        taskFormData.append('task_type_code', task.task_type_code );
        taskFormData.append('performer_number', task.performer_id);


        await axios.post(url_for_task_add, taskFormData, this.getConfig)

        this.tasks = []

        await this.getTasks()

        this.add_task_dialog_visible = false
      }
      catch (e){
          console.log(e)
      }

    },

    // парсинг самих заданий
    async getTasks(){
      try {
        if (!this.$store.state.loggedIn) return router.push('/')

        const response = await axios.get(process.env.VUE_APP_API + '/tasks/?username='
            + localStorage.getItem('username') + '&password=' + localStorage.getItem('password'), this.getConfig)
        const array = response.data['tasks']

        array.forEach((element)=> {
          const newTask = {
            id: element['task_number'],
            author_number:element['author_number'],
            contact_number: element['contact_number'],
            date_of_completion: element['date_of_completion'],
            date_of_creation: element['date_of_creation'],
            performer_number: element['performer_number'],
            priority_code: element['priority_code'],
            status: element['status'],
            task_type_code: element['task_type_code'],
            term_of_execution: element['term_of_execution']
          }
          if (newTask.contact_number !== null){
            newTask.contact_number = {
              contract_number: element['contract_number'],
              contract_details: element['contract_details'],
              vin: element['vin'],
              license_plate: element['license_plate']
            }
          }

          if (newTask['status'] === 0){
            newTask['status'] = 'в процессе'
          }
          else {
            newTask['status'] = 'завершено'
          }
          this.tasks.push(newTask)

        })

      }
      catch (e){
        alert('Неверный логин или пароль')
      }

      if (this.priority_codes.length === 0){
        await this.getTasksTypeClassifier()
      }

      if (this.tasks_type_classifier.length === 0){
        await this.getTasksClassifier()
      }

      if (this.employees.length === 0){
        await this.getEmployees()
      }

      this.tasks.forEach((element) =>{
        element.priority_code = this.priority_codes.find(el => el.id === element.priority_code)['value']
        element.task_type_code = this.tasks_type_classifier.find(el => el.id === element.task_type_code)['value']

      })

      if (this.dbRole === ''){
        try{
          const roleResponse = await axios.get(process.env.VUE_APP_API + '/users/?login=' + localStorage.getItem('username'), this.getConfig)
          this.dbRole = roleResponse.data['iAm']['role']

        }
        catch (e){
          alert('Ошибка во время присвоения роли')
        }
      }

    },

    // парсинг классификатора заданий
    async getTasksClassifier(){
      try {
        if (this.tasks_type_classifier.length === 0){
          // cassifier??? Кирюх, не болей дислексией, пжлст
          let response = await axios.get(process.env.VUE_APP_API + '/tasks_cassifier/', this.getConfig)
          if(response.status !== 200) {
            response = await axios.get(process.env.VUE_APP_API + '/tasks_classifier/', this.getConfig)
          }
          const array = response.data['tasks classifier']
          array.forEach((element)=> {
            const newTaskClassifier = {
              id:element["task_type_code"],
              value: element["task_type"]
            }
            this.tasks_type_classifier.push(newTaskClassifier)
          })
        }
      }
      catch (e){
        console.log('Ошибка при загрузке классификаторов')
        console.log(process.env.VUE_APP_API)
      }
    },

    // парсинг классификатора приоритетов заданий
    async getTasksTypeClassifier(){
      try {
          if (this.priority_codes.length === 0){
            const response = await axios.get(process.env.VUE_APP_API + '/tasks_priority/', this.getConfig)
            const array = response.data['tasks priority']
            array.forEach((element)=> {
              const newPriority = {
                id:element["priority_code"],
                value: element["classifier"]
              }
              this.priority_codes.push(newPriority)
            })
          }
      }
      catch (e){
        console.log('Ошибка во время загрузки классификатора приоритетов')
      }
    },

    // парсинг работников
    async getEmployees(){
      try {
        const response = await axios.get(process.env.VUE_APP_API + '/employees/?username='
            + localStorage.getItem('username') + '&password=' + localStorage.getItem('password'), this.getConfig)
        const array = response.data['employees']

        array.forEach((element)=> {
          const newEmployee = {
            id: element['employee_id'],
            value: element['login'],  // value = login
          }
          this.employees.push(newEmployee)
        })

        this.tasks.forEach((element) =>{
          if (element.author_number !== null) {
            element.author_number = this.employees.find(el => el.id === element.author_number)['value']
          }
          if (element.performer_number !== null) {
            element.performer_number = this.employees.find(el => el.id === element.performer_number)['value']
          }
        })
      }
      catch (e){
        alert('error')
      }
    },

    // Пока что в виде JSON, может быть сделаю потом конвертацию в Excel
    exportTasks(){
      const data = JSON.stringify(this.tasks)
      const blob = new Blob([data], {type: 'application/json'})
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'tasks.json')
      document.body.appendChild(link)
      link.click()
      link.remove()
    },
  },

  // Эта штука позволяет нам отображать таски до того, как страница загрузится
  beforeMount() {
    this.getTasks()
  }
}
</script>

<style>
.task-headers{
  display: flex;
  align-items: center;
}
.task-buttons{
  margin-left: auto;
  display: flex;
}
</style>