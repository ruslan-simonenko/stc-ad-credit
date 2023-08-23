<template>
  <q-header elevated>
    <q-toolbar>
      <q-btn flat round dense icon="menu" class="q-mr-sm" @click="navigationPanelVisible = !navigationPanelVisible">
      </q-btn>
      <q-separator dark vertical inset/>
      <q-img src="https://www.seethroughcarbon.org/favicon.ico" width="2.5em" class="q-ml-md"></q-img>
      <q-toolbar-title>STC - Ad Credit</q-toolbar-title>
      <UserInfoButton></UserInfoButton>
    </q-toolbar>
  </q-header>
  <q-drawer
      v-model="navigationPanelVisible"
      show-if-above
      bordered
      :width="200"
      :breakpoint="800">
    <NavigationList/>
  </q-drawer>
</template>

<script setup lang="ts">
import UserInfoButton from "./UserInfoButton.vue";
import {ref} from "vue";
import NavigationList from "./NavigationList.vue";

const navigationPanelVisible = ref<boolean>(false)
</script>