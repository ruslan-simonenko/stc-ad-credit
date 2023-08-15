<template>
  <a :href="businessLink">Business Profile</a>
</template>

<script setup lang="ts">
import {useBrowserLocation} from "@vueuse/core";
import {computed} from "vue";
import {useApiClientAxios} from "../../../api/api-client-axios.ts";

const props = defineProps({
  businessID: Number
})

const apiClient = useApiClientAxios();
const location = useBrowserLocation();

const businessLink = computed(() => `${location.value.origin}${apiClient.defaults.baseURL}/businesses/${props.businessID}/profile`)
</script>

<style scoped>

</style>