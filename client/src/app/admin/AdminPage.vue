<template>
  <q-page padding>
    <CarbonAuditorsList></CarbonAuditorsList>
    <UserManagementList></UserManagementList>
  </q-page>
</template>

<script setup lang="ts">
import CarbonAuditorsList from "../carbon-auditor/CarbonAuditorsList.vue";
import UserManagementList from "../../user/UserManagementList.vue";
</script>
