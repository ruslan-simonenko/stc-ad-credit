<template>
  <q-table
      flat bordered
      :rows="adRecordsStore.all.items"
      :columns="columns"
      :rows-per-page-options="[10, 25, 50, 100]"
      :visible-columns="visibleColumns"
  >
    <template v-slot:top>
      <div class="text-h6">Ad Records</div>
      <q-btn label="Add" v-if="authStore.hasRole(UserRole.AD_MANAGER)"
             color="primary" class="q-ml-sm"
             @click="goToAdRecordAddPage"/>
    </template>
    <template v-slot:body-cell-business="props">
      <q-td :props="props">
        {{ props.value.name }}
      </q-td>
    </template>
    <template v-slot:body-cell-creator="props">
      <q-td :props="props">
        {{ props.value?.name ?? props.value?.email }}
      </q-td>
    </template>
  </q-table>
</template>

<script setup lang="ts">
import {User, UserRole} from "../../../user/user.ts";
import {AdRecord} from "./ad-records-types.ts";
import {useBusinessStore} from "../../business/business-store.ts";
import {onMounted} from "vue";
import {useAdRecordsStore} from "./ad-records-store.ts";
import {Business} from "../../business/business-types.ts";
import {useUserStore} from "../../../user/user-store.ts";
import {useAuthStore} from "../../../auth/auth-store.ts";
import {QTableProps} from "quasar";
import {useRouter} from "vue-router";

const businessStore = useBusinessStore();
const adRecordsStore = useAdRecordsStore();
const userStore = useUserStore();
const authStore = useAuthStore();

const router = useRouter();

const goToAdRecordAddPage = () => router.push({name: 'AdRecordAdd'});


const columns: QTableProps['columns'] = [
  {
    name: 'business',
    label: 'Business',
    align: 'left',
    field: (record: AdRecord): Business => businessStore.all.items.find(business => business.id == record.business_id)!
  },
  {name: 'ad_post_url', label: 'Ad', align: 'left', field: (record: AdRecord): string => record.ad_post_url},
  {
    name: 'creator',
    label: 'Created By',
    align: 'left',
    field: (record: AdRecord): User => userStore.all.items.find(user => user.id == record.creator_id)!
  },
  {
    name: 'timestamp',
    label: 'Created At',
    align: 'right',
    field: (record: AdRecord): Date => record.created_at,
    format: (value: Date) => value.toLocaleString()
  },
];
const visibleColumns = [
  'business', 'ad_post_url',
  ...(authStore.hasRole(UserRole.ADMIN) ? ['creator'] : []),
  'timestamp'
]

onMounted(() => {
  businessStore.fetch()
  adRecordsStore.fetch()
  userStore.fetch()
});
</script>

<style scoped>

</style>