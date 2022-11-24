<template>
  <main class="layout">
    <div class="client-header">
      <h2>Список клиентов</h2>
      <input type="text" v-model="search" style="margin-left: 2rem" placeholder="Найти клиента..."/>
    </div>
    <transition-group name="post-list">
      <client-item v-for="client in filteredList"
                   :clients="client"
                   :key="client.contact_person_number"
      />
    </transition-group>
  </main>
</template>
<script>
import axios from "axios";
import ClientItem from "@/components/ClientItem";

export default {
  name: "clients-page",
  components: {ClientItem},
  computed: {
    getConfig() {
      return this.$store.getters.getConfig;
    },
    filteredList() {
      return this.clients.filter(client => {
        return client.contact_person_name.toLowerCase().includes(this.search.toLowerCase())
      })
    }
  },

  data(){
    return {
      search: '',
      clients: [],
      organizations: [],
    };
  },

  methods: {
    // Получение списка клиентов, к которому у меня нет доступа :(
    async getOrganizations() {
      try {
        const response = await axios.get(process.env.VUE_APP_API + '/organizations/', this.getConfig);
        const array = response.data['Organizations'];
        array.forEach((element)=> {
          const newPriority = {
            organization_number:element["organization_number"],
            organization_name: element["organization_name"],
            client_type: element["client_type"],
          }
          this.organizations.push(newPriority)
        })
      } catch (e) {
        alert('Ошибка при получении списка организаций')
      }
    },
    async getClients() {
      try {
        const response = await axios.get(process.env.VUE_APP_API + '/contact_numbers', this.getConfig);

        const allClients = response.data['Contact persons'];
        allClients.forEach((client) => {
          const clientItem = {
            contact_person_number: client['contact_person_number'],
            contact_person_name: client['contact_person_name'],
            phone: client['phone'],
            email: client['email'],
            city: client['city'],
            organization_number: client['organization_number'],
          }
          this.clients.push(clientItem);
        });
      } catch (e) {
        alert('Ошибка при получении клиентов');
      }
    },
  },

  beforeMount() {
    this.getClients();
  }
}
</script>

<style>
.client-header{
  display: flex;
  align-items: center;
}
</style>