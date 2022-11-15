<template>
  <div>
    <div class="task__worker">
      <h3> List of tasks</h3>
      <button type="button"
              @click="$emit('create_task')"
              class="btn btn-warning">Create Task</button>
    </div>
      <transition-group name="post-list">
        <my-task-item v-for="task in tasks"
                   :task="task"
                   :key="task.id"
                      @show_task_changer="$emit('show_task_changer', task)"
        />
      </transition-group>
  </div>
</template>

<script>
import MyTaskItem from "@/components/UA/TaskItem";
export default {
  name: "my-tasks-list",
  components: {MyTaskItem},
  props:{
    tasks:{
      type: Array,
      required: true
    }
  },
}
</script>

<style scoped>
.task__worker{
  display: flex;
  margin: 15px;
  align-items: center;
}

/* Это на будущее что-то?           *
 * TODO: Проверить что это за фигня */
.task-list-item{
  display: inline-block;
  margin-right: 10px;
}
.task-list-enter-active,
.task-list-leave-active{
  transition: all 0.4s ease;
}
.task-list-enter-form,
.task-list-leave-to{
  opacity: 0;
  transform: translateY(30px);
}
.task-list-move{
  transition: transform .4s ease;
}
</style>