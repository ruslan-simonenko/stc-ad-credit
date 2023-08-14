<template>
  <q-page padding>
    <div class="column q-gutter-y-md">
      <AdRecordAddForm v-if="isAdManager"/>
      <AdRecordsTable/>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import AdRecordAddForm from "./AdRecordAddForm.vue";
import AdRecordsTable from "./AdRecordsTable.vue";
import {useAuthStore} from "../../../auth/auth-store.ts";
import {UserRole} from "../../../user/user.ts";
import {computed} from "vue";

const authStore = useAuthStore();

const isAdManager = computed<boolean>(() => authStore.hasRole(UserRole.AD_MANAGER))
</script>