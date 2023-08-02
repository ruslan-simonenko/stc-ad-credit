<template class="relative-position">
  <q-list>
    <q-item>
      <BusinessAddForm/>
    </q-item>
    <!-- Loaded -->
    <template v-if="state == State.LOADED">
      <template v-for="(business, index) in businessStore.all.items">
        <q-separator v-if="index !== 0" spaced inset/>
        <q-item>
          <q-item-section>
            <q-item-label>{{ business.name }}</q-item-label>
            <q-item-label v-if="business.facebook_url">{{ business.facebook_url }}</q-item-label>
          </q-item-section>
        </q-item>
      </template>
    </template>
    <!-- Loading -->
    <q-inner-loading :showing="state == State.LOADING" label="Please wait..."/>
    <!-- Error -->
    <q-item v-if="state == State.ERROR">
      <q-item-section class="error-background"></q-item-section>
    </q-item>
    <q-inner-loading :showing="state == State.ERROR">
      <div class="column items-center">
        <q-icon name="warning" color="warning" size="4rem"></q-icon>
        <span class="text-dark">Can't load the data</span>
        <q-btn flat color="primary" label="Try again" @click="businessStore.fetch()"></q-btn>
      </div>
    </q-inner-loading>
  </q-list>
</template>

<script setup lang="ts">
import {useBusinessStore} from "./business-store.ts";
import BusinessAddForm from "./BusinessAddForm.vue";
import {computed, onMounted} from "vue";

const businessStore = useBusinessStore()

onMounted(() => {
  businessStore.fetch()
});

enum State {
  LOADED, LOADING, ERROR
}

const state = computed<State>(() => {
  if (businessStore.all.fetching) {
    return State.LOADING
  }
  if (businessStore.all.error) {
    return State.ERROR
  }
  return State.LOADED
});
</script>

<style scoped>
.error-background {
  height: 10rem
}
</style>