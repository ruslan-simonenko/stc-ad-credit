<template class="relative-position">
  <q-table
      flat bordered
      :grid="$q.screen.lt.md"
      :rows="businessStore.all.items"
      :columns="columns"
      :loading="loading"
      row-key="id">
    <template v-slot:top>
      <div class="text-h6">Businesses</div>
      <q-btn label="Add" v-if="canAdd" :disable="loading"
             color="primary" class="q-ml-sm"
             @click="goToBusinessAddPage"/>
    </template>
    <template v-if="authStore.hasRole(UserRole.ADMIN)" v-slot:body-cell-score="props">
      <q-td :props="props">
        <div class="row inline items-end">
          <div v-if="props.value != null" style="margin-right: .5em">{{ props.value }}</div>
          <CarbonAuditSentimentIcon :score="props.value" size="2em"/>
        </div>
      </q-td>
    </template>
    <template v-if="canEdit" v-slot:body-cell-actions="props">
      <q-td :props="props">
        <div class="row inline">
          <q-btn @click="edit(props.value)">Edit</q-btn>
        </div>
      </q-td>
    </template>
    <template v-slot:item="props">
      <div class="q-pa-xs col-xs-12 col-sm-6">
        <q-card bordered flat>
          <q-card-section horizontal>
            <q-list class="col" dense>
              <q-item v-for="column in props.cols.filter((column_: any) => column_.name != Columns.ACTIONS)"
                      :key="column.name">
                <q-item-section>
                  <q-item-label caption>{{ column.label }}</q-item-label>
                  <q-item-label v-if="column.name != Columns.SCORE">{{ column.value }}</q-item-label>
                  <template v-else>
                    <div class="row inline items-center">
                      <CarbonAuditSentimentIcon :score="column.value" size="2em"/>
                      <div v-if="column.value != null" class="q-ml-xs">{{ column.value }}</div>
                    </div>
                  </template>
                </q-item-section>
              </q-item>
            </q-list>
            <q-card-actions v-if="canEdit" vertical>
              <q-btn round flat icon="more_vert">
                <q-menu auto-close anchor="bottom end" self="top end">
                  <q-list>
                    <q-item clickable @click="edit(props.row!)">
                      <q-item-section>Edit</q-item-section>
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
import {useBusinessStore} from "./business-store.ts";
import {computed, onMounted} from "vue";
import {useCarbonAuditStore} from "../carbon-audit/carbon-audit-store.ts";
import {Business} from "./business-types.ts";
import {useAdAllowanceStore} from "../ad/allowance/ad-allowance-store.ts";
import {AdAllowance} from "../ad/allowance/ad-allowance-types.ts";
import {useAdStrategyStore} from "../ad/strategy/ad-strategy-store.ts";
import {QTableProps} from "quasar";
import {useAuthStore} from "../../auth/auth-store.ts";
import {UserRole} from "../../user/user.ts";
import {useRouter} from "vue-router";
import CarbonAuditSentimentIcon from "../carbon-audit/components/CarbonAuditSentimentIcon.vue";

const authStore = useAuthStore();
const businessStore = useBusinessStore();
const auditStore = useCarbonAuditStore();
const adAllowanceStore = useAdAllowanceStore();
const adStrategyStore = useAdStrategyStore();

const router = useRouter();

const goToBusinessAddPage = () => router.push({name: 'BusinessAdd'});

const loading = computed<boolean>(() => businessStore.all.fetching || auditStore.all.fetching || adAllowanceStore.data.fetching || adStrategyStore.data.fetching)

const canAdd = computed<boolean>(() => authStore.hasRole(UserRole.BUSINESS_MANAGER) || authStore.hasRole(UserRole.AD_MANAGER));
const canEdit = computed<boolean>(() => authStore.hasRole(UserRole.BUSINESS_MANAGER) || authStore.hasRole(UserRole.AD_MANAGER));

enum Columns {
  NAME = 'name',
  REGISTRATION = 'registration',
  EMAIL = 'email',
  SCORE = 'score',
  ALLOWANCE = 'allowance',
  FACEBOOK_URL = 'facebook_url',
  ACTIONS = 'actions',
}

const ColumnsOrder: Array<string> = [Columns.NAME, Columns.FACEBOOK_URL, Columns.SCORE, Columns.ALLOWANCE, Columns.REGISTRATION, Columns.EMAIL, Columns.ACTIONS];

const prepareColumns = (): QTableProps['columns'] => {
  const COLUMN_ACTIONS: QTableProps['columns'] = [{
    name: Columns.ACTIONS,
    label: 'Actions',
    align: 'left',
    field: (row: Business) => row,
  }];

  const businessManagerColumns: QTableProps['columns'] = authStore.hasRole(UserRole.BUSINESS_MANAGER) ? [
    {
      name: Columns.REGISTRATION,
      label: 'Registration',
      align: 'left',
      field: (row: Business) => row.sensitive,
      format: (sensitiveData: Business['sensitive']) => `${sensitiveData!.registration_type} ${sensitiveData!.registration_number}`
    },
    {
      name: Columns.EMAIL,
      label: 'Contact Email',
      align: 'left',
      field: (row: Business) => row.sensitive,
      format: (sensitiveData: Business['sensitive']) => sensitiveData!.email
    },
    ...COLUMN_ACTIONS,
  ] : [];

  const adManagerColumns: QTableProps['columns'] = authStore.hasRole(UserRole.AD_MANAGER) ? [
    ...COLUMN_ACTIONS,
  ] : [];

  const adminColumns: QTableProps['columns'] = authStore.hasRole(UserRole.ADMIN) ? [
    {
      name: Columns.SCORE,
      label: 'Carbon Audit Score',
      field: (row: Business) => auditStore.all.items.find(audit => audit.business_id === row.id)?.score ?? null,
    },
    {
      name: Columns.ALLOWANCE,
      label: 'Ads Used',
      field: (row: Business) => adAllowanceStore.data.indexed[row.id],
      format: (value: AdAllowance | null): string => value != null ? `${value.used_allowance} / ${value.allowance}` : ''
    }] : [];
  const columns: QTableProps['columns'] = [
    {
      name: Columns.NAME,
      label: 'Name',
      align: 'left',
      field: (row: Business) => row.name,
    },
    {
      name: Columns.FACEBOOK_URL,
      label: 'Facebook URL',
      align: 'left',
      field: (row: Business) => row.facebook_url,
    },
    ...adminColumns,
    ...adManagerColumns,
    ...businessManagerColumns,
  ];
  columns.sort((colA, colB) => ColumnsOrder.indexOf(colA.name) - ColumnsOrder.indexOf(colB.name))
  return columns;
}

const columns: QTableProps['columns'] = prepareColumns();

const edit = async (business: Business) => await router.push({name: "BusinessEdit", params: {id: business.id}});

onMounted(() => {
  businessStore.fetch()
  if (authStore.hasRole(UserRole.ADMIN)) {
    auditStore.fetch()
    adAllowanceStore.fetch()
    adStrategyStore.fetch()
  }
});
</script>

<style scoped>
</style>