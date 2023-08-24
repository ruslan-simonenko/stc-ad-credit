<template>
  <q-form @submit="onSubmit" class="q-gutter-md">
    <q-input
        type="email"
        v-model="data.email"
        label="Email"
        :rules="emailValidators"
    />
    <q-option-group
        v-model="data.roles"
        :options="roleOptions"
        type="toggle"
    />
    <q-btn :label="props.id==null ? 'Add User' : 'Update User'" type="submit" color="primary"/>
  </q-form>
</template>

<script setup lang="ts">
import {computed, onMounted, shallowReactive, watch} from "vue";
import {useUserStore} from "../user-store.ts";
import {User, UserRole} from "../user.ts";
import {QForm} from "quasar";
import {fieldRequiredValidator} from "../../utils/form-validators.ts";
import {z} from "zod";

const DataSchema = z.object({email: z.string(), roles: z.array(z.nativeEnum(UserRole))});
type Data = z.TypeOf<typeof DataSchema>;
const EMPTY_DATA = {email: '', roles: []};

const userStore = useUserStore();

const props = defineProps({id: Number});
const emit = defineEmits(['submit']);

const user = computed(() => userStore.all.items.find(user => user.id == props.id));

const data = shallowReactive<Data>(DataSchema.parse(EMPTY_DATA));
const updateData = (newData: Data) => {
  const newDataCopy = DataSchema.parse(newData);
  data.email = newDataCopy.email;
  data.roles = newDataCopy.roles;
}
watch(
    () => user.value,
    (user: User | undefined) => updateData(user ?? EMPTY_DATA),
    {immediate: true});

const roleOptions = Object.values(UserRole).map(role => ({label: role, value: role}))
const emailValidators = [fieldRequiredValidator];

const onSubmit = async () => {
  if (props.id == null) {
    await userStore.add(data);
  } else {
    await userStore.update(props.id, data);
  }
  resetForm()
  emit('submit');
}

const resetForm = () => updateData(EMPTY_DATA);

onMounted(() => {
  userStore.fetch();
});
</script>

<style scoped>

</style>