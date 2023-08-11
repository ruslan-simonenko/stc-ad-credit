<template>
  <q-page padding>
    <div class="q-gutter-y-lg">
      <UserAddForm></UserAddForm>
      <UsersTable></UsersTable>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import UsersTable from "../../user/management/UsersTable.vue";
import UserAddForm from "../../user/management/UserAddForm.vue";
</script>
