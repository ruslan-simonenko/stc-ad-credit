<template>
  <q-table
      title="Users"
      :rows="userStore.all.items"
      :columns="columns"
      :loading="userStore.all.fetching"
  />
</template>

<script setup lang="ts">
import {useUserStore} from "../user-store.ts";
import {User} from "../user.ts";
import {onMounted} from "vue";

const userStore = useUserStore();

const columns = [
  {name: 'name', label: 'Name', align: 'left', field: (user: User) => user.name},
  {name: 'email', label: 'E-mail', align: 'left', field: (user: User) => user.email},
  {name: 'roles',label: 'Roles', align: 'left', field: (user: User) => user.roles},
  {name: 'actions', },
]

onMounted(() => {
  userStore.fetch()
});
</script>

<style scoped>

</style>