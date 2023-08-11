<template>
  <q-page padding>
    <UserManagementList></UserManagementList>
    <UsersTable></UsersTable>
  </q-page>
</template>

<script setup lang="ts">
import UserManagementList from "../../user/management/UserManagementList.vue";
import UsersTable from "../../user/management/UsersTable.vue";
</script>
