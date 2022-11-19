<template>
  <navbar>
    <div  v-if="tasks.length !== 0" class="btn__input">
      <button type="button"
              v-if="dbRole === 'administrator' "
              style="margin-left: 20px"
              @click="addUserDialog"
              class="btn btn-warning">Создать пользователя</button>

      <button type="button"
              style="margin-left: 20px"
              @click="changeUser"
              class="btn btn-warning">Выйти</button>
    </div>
  </navbar>

  <div class="app">
    <div v-if="isLogin === false">
      <div class="input__auth">
        <base-input v-model="username"
                  placeholder="Логин"/>
        <!--
        Не совсем понимаю зачем делать отдельный input, если можно использовать обычный со стилем
        Но ладно, хрен с тобой
        -->
        <base-input v-model="password"
                  placeholder="Пароль" type="password"/>
      </div>

      <div>
        <button type="button" @click="getTasks"
                class="btn btn-success">Войти</button>
      </div>
    </div>
    <div v-else>
      <task-list :tasks="tasks"
                     @create_task="createTaskDialog"
      />

      <base-dialog v-model:show="add_dialog_visible">
        <user-create-popup :roles="allDbRoles" @createUser="createUser"/>
      </base-dialog>

      <base-dialog v-model:show="add_task_dialog_visible">
        <task-create-popup :all_priority_codes="priority_codes"
                        :all_task_type_codes="tasks_type_classifier"
                        :all_employees="employees"
                        :role="dbRole"
                        @createTask="createTask"
        />
      </base-dialog>

    </div>
  </div>
</template>

<script>

import axios from "axios";
import TaskList from "@/components/TaskList";
import BaseInput from "@/components/BaseInput";
import UserCreatePopup from "@/components/UserCreatePopup";
import TaskCreatePopup from "@/components/TaskCreatePopup";
import NavBar from "@/components/NavBar";


export default {
  name: "main-page",
  components: {
    TaskCreatePopup,
    UserCreatePopup,
    BaseInput,
    TaskList,
    NavBar
  },


  data(){
    return{
      username: 'nick',
      password: 'qwerty',

      isLogin: false,

      // Ну так-то это в бэкенде должно быть
      allDbRoles: [
        {id: 1, value:'worker'},
        {id: 2, value:'manager'},
        {id: 3, value:'administrator'},
      ],

      dbRole: '',

      tasks: [],
      tasks_type_classifier: [],
      contracts: [],
      employees: [],
      priority_codes: [],
      config: {
        headers:{
          // ХАРДКОД (╯°□°）╯︵ ┻━┻
          'Authorization': 'Token e222cdf2fae4ff2e6494640269f150b4ff52f468'
        }
      },
      // видимость диалогов
      add_dialog_visible: false,
      add_task_dialog_visible: false,

      // для выпадающих списков
      priorityCodeSort: ''


    }
  },

  methods:{
    changeUser(){
      this.username = ''
      this.password = ''
      this.dbRole = ''
      this.tasks = []
      this.isLogin = false
    },

    addUserDialog(){
      this.add_dialog_visible = true
    },

    createTaskDialog(){
      this.add_task_dialog_visible = true
    },

    // создание нового задания
    async createTask(task){

      try {
        if (task.contract_number !== null) {
          const contract_url = process.env.VUE_APP_API + '/contracts/?username=' + this.username + '&password=' + this.password
          let formData = new FormData();

          formData.append('contract_details', task.contract_number.contract_details);
          formData.append('vin', task.contract_number.vin);
          formData.append('license_plate', task.contract_number.license_plate);


          const response = await axios.post(contract_url, formData, this.config)

          task.contract_number = response.data['id'][0][0]
        }

        const url_for_task_add = process.env.VUE_APP_API + '/tasks/?username=' + this.username + '&password=' + this.password

        console.log(task)

        let taskFormData = new FormData();

        taskFormData.append('term_of_execution', task.term_of_execution);
        taskFormData.append('contract_number', task.contract_number);
        taskFormData.append('priority_code', task.priority_code);
        taskFormData.append('task_type_code', task.task_type_code );
        taskFormData.append('performer_number', task.performer_id);


        await axios.post(url_for_task_add, taskFormData, this.config)

        this.tasks = []

        await this.getTasks()

        this.add_task_dialog_visible = false
      }
      catch (e){
          console.log(e)
      }

    },

    // создание нового пользователя
    async createUser(user) {
      try {

        const url = process.env.VUE_APP_API + '/users/?username=' + this.username + '&password=' + this.password

        let formData = new FormData();

        formData.append('login', user['login']);
        formData.append('password', user['password']);
        formData.append('name', user['user_name']);
        formData.append('role', user['role']);


        const response = await axios.post(url, formData, this.config)


        if (response.data === 200){
          alert(e)
        }
        else {
          this.add_dialog_visible = false
        }

      } catch (e) {
        alert(e)
      }
    },

    // парсинг самих заданий
    async getTasks(){
      try {
        const response = await axios.get(process.env.VUE_APP_API + '/tasks/?username=' + this.username + '&password=' + this.password, this.config)
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
        this.isLogin = true

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
          const roleResponse = await axios.get(process.env.VUE_APP_API + '/users/?login=' + this.username, this.config)
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
          let response = await axios.get(process.env.VUE_APP_API + '/tasks_cassifier/', this.config)
          if(response.status !== 200) {
            response = await axios.get(process.env.VUE_APP_API + '/tasks_classifier/', this.config)
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
            const response = await axios.get(process.env.VUE_APP_API + '/tasks_priority/', this.config)
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
        const response = await axios.get(process.env.VUE_APP_API + '/employees/?username=' + this.username + '&password=' + this.password, this.config)
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
            element.author_number = this.employees.find(el => el.id === element.author_number)['login']
          }
          if (element.performer_number !== null) {
            element.performer_number = this.employees.find(el => el.id === element.performer_number)['login']
          }
        })
      }
      catch (e){
        alert('error')
      }
    },

  },

}
</script>

<style>
.input__auth{
  margin-left: 5px;
}
.btn {
  margin-left: auto;
  display: flex;
  background-color: #00abc3;
  border-color: #00abc3;
  color: #fff;
}
.btn:hover {
  background-color: #00a896;
  border-color: #00a896;
}
.btn__input{
  display: flex;
}

</style>