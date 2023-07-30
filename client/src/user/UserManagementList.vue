<template>
  <q-list class="relative-position" bordered padding>
    <q-item-label header>Users</q-item-label>
    <q-separator inset/>
    <q-item>
      <UserAddForm></UserAddForm>
    </q-item>
    <q-separator inset/>
    <!-- Loaded -->
    <q-item v-if="state == State.LOADED" v-for="user in userStore.all.items">
      <q-item-section avatar>
        <q-avatar size="3rem"><img :src="user.picture_url"></q-avatar>
      </q-item-section>
      <q-item-section>
        <q-item-label>{{ user.name }}</q-item-label>
        <q-item-label>{{ user.email }}</q-item-label>
      </q-item-section>
    </q-item>
    <!-- Loading -->
    <q-item v-if="state == State.LOADING" v-for="_ in 4">
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
    <q-inner-loading :showing="state == State.LOADING" label="Please wait..."/>
    <!-- Error -->
    <q-item v-if="state == State.ERROR">
      <q-item-section class="error-background"></q-item-section>
    </q-item>
    <q-inner-loading :showing="state == State.ERROR">
      <div class="column items-center">
        <q-icon name="warning" color="warning" size="4rem"></q-icon>
        <span class="text-dark">Can't load the data</span>
        <q-btn flat color="primary" label="Try again" @click="userStore.fetch"></q-btn>
      </div>
    </q-inner-loading>
  </q-list>
</template>

<script setup lang="ts">

import {useUserStore} from "./user-store.ts";
import {computed, onMounted} from "vue";
import UserAddForm from "./UserAddForm.vue";

const userStore = useUserStore();

onMounted(() => {
  userStore.fetch()
})

enum State {
  LOADED, LOADING, ERROR
}

const state = computed<State>(() => {
  if (userStore.all.fetching) {
    return State.LOADING
  }
  if (userStore.all.error) {
    return State.ERROR
  }
  return State.LOADED
})
</script>

<style scoped>

</style>