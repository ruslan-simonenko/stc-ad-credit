<template>
  <q-table
      flat bordered
      :grid="$q.screen.lt.md"
      :rows="userStore.all.items"
      :columns="columns"
      :loading="userStore.all.fetching"
      :rows-per-page-options="[10, 25, 50, 100]"
  >
    <template v-slot:top>
      <div class="text-h6">Users</div>
      <q-btn label="Add" v-if="authStore.hasRole(UserRole.ADMIN)"
             color="primary" class="q-ml-sm"
             @click="goToUserAddPage"/>
    </template>
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
    <!-- Grid mode -->
    <template v-slot:item="props">
      <div class="q-pa-xs col-xs-12 col-sm-6 grid-style-transition">
        <q-card bordered flat>
          <q-card-section horizontal>
            <q-list class="col" dense>
              <q-item v-for="column in props.cols.filter(column => column.name != 'actions')" :key="column.name">
                <q-item-section>
                  <q-item-label caption>{{ column.label }}</q-item-label>
                  <q-item-label>{{ column.value }}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
            <q-card-actions v-if="authStore.hasRole(UserRole.ADMIN)" vertical>
              <q-btn round flat icon="more_vert">
                <q-menu auto-close anchor="bottom end" self="top end">
                  <q-list>
                    <q-item clickable @click="loginAs(props.row!)">
                      <q-item-section>Login as</q-item-section>
                    </q-item>
                  </q-list>
                </q-menu>
              </q-btn>
            </q-card-actions>
          </q-card-section>
        </q-card>
      </div>
    </template>
  </q-table>
</template>

<script setup lang="ts">
import {useUserStore} from "../user-store.ts";
import {User, UserRole} from "../user.ts";
import {onMounted} from "vue";
import {useAuthStore} from "../../auth/auth-store.ts";
import {useRouter} from "vue-router";
import {QTableProps} from "quasar";

const userStore = useUserStore();
const authStore = useAuthStore();
const router = useRouter();

const goToUserAddPage = () => router.push({name: 'UserAdd'});

const columns: QTableProps['columns'] = [
  {name: 'name', label: 'Name', align: 'left', field: (user: User) => user.name},
  {name: 'email', label: 'E-mail', align: 'left', field: (user: User) => user.email},
  {
    name: 'roles',
    label: 'Roles',
    align: 'left',
    field: (user: User) => user.roles,
    format: (roles: Array<UserRole>) => roles.join(', ')
  },
  {name: 'actions', label: 'Actions', align: 'left', field: (user: User) => user},
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