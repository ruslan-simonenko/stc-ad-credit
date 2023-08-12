<template>
  <q-table
      title="Users"
      :rows="userStore.all.items"
      :columns="columns"
      :loading="userStore.all.fetching"
      :rows-per-page-options="[10, 25, 50, 100]"
  >
    <template v-slot:body-cell-name="props">
      <q-td :props="props" class="q-gutter-xs">
        <q-avatar square size="3rem">
          <img v-if="props.row!.picture_url" :src="props.row!.picture_url">
        </q-avatar>
        <span>{{ props.row!.name }}</span>
      </q-td>
    </template>
    <template v-slot:body-cell-actions="props">
      <q-td :props="props">
        <q-btn v-if="authStore.hasRole(UserRole.ADMIN)" @click="loginAs(props.row!)">Login as</q-btn>
      </q-td>
    </template>
  </q-table>
</template>

<script setup lang="ts">
import {useUserStore} from "../user-store.ts";
import {User, UserRole} from "../user.ts";
import {onMounted} from "vue";
import {useAuthStore} from "../../auth/auth-store.ts";
import {useRouter} from "vue-router";

const userStore = useUserStore();
const authStore = useAuthStore();
const router = useRouter();

const columns = [
  {name: 'name', label: 'Name', align: 'left', field: (user: User) => user.name},
  {name: 'email', label: 'E-mail', align: 'left', field: (user: User) => user.email},
  {
    name: 'roles',
    label: 'Roles',
    align: 'left',
    field: (user: User) => user.roles,
    format: (roles: Array<UserRole>) => roles.join(', ')
  },
  {name: 'actions', label: 'Actions', align: 'left'},
]

const loginAs = async (user: User) => {
  await authStore.loginAs(user)
  await router.push({name: "Home"})
}


onMounted(() => {
  userStore.fetch()
});
</script>

<style scoped>

</style>