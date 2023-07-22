<template>
  <q-list class="relative-position" bordered padding>
    <q-item-label header>Carbon Auditors</q-item-label>
    <!-- Loaded -->
    <q-item v-if="!isLoading" v-for="auditor in auditorStore.all.items">
      <q-item-section avatar>
        <q-avatar size="3rem"><img :src="auditor.picture_url"></q-avatar>
      </q-item-section>
      <q-item-section>
        <q-item-label>{{ auditor.name }}</q-item-label>
        <q-item-label>{{ auditor.email }}</q-item-label>
      </q-item-section>
    </q-item>
    <!-- Loading -->
    <q-item v-if="isLoading" v-for="_ in 4">
      <q-item-section avatar>
        <q-skeleton type="QAvatar" size="3rem"/>
      </q-item-section>
      <q-item-section>
        <q-item-label>
          <q-skeleton type="text" width="7rem"/>
        </q-item-label>
        <q-item-label>
          <q-skeleton type="text" width="12rem"/>
        </q-item-label>
      </q-item-section>
    </q-item>
    <q-inner-loading
        :showing="isLoading"
        label="Please wait..."
    />
  </q-list>
</template>

<script setup lang="ts">
import {useCarbonAuditorStore} from "./carbon-auditor-store.ts";
import {computed, onMounted} from "vue";

const auditorStore = useCarbonAuditorStore();

onMounted(() => {
  auditorStore.fetch()
})

const isLoading = computed(() => auditorStore.all.fetching)
</script>
