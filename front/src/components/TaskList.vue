<template>
  <div>
      <transition-group name="post-list">
        <task-item v-for="task in tasks"
                   :task="task"
                   :key="task.id"
                      @show_task_changer="$emit('show_task_changer', task)"
        />
      </transition-group>
  </div>
</template>

<script>
import TaskItem from "@/components/TaskItem";
export default {
  name: "task-list",
  components: {TaskItem},
  props:{
    tasks:{
      type: Array,
      required: true
    }
  },
}
</script>

<style scoped>

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