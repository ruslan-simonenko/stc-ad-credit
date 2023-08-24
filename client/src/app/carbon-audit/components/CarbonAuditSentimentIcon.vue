<template>
  <q-skeleton v-if="rating == Rating.PENDING" type="circle" :size="props.size"/>
  <q-icon v-else :name="RatingData[rating]!.icon" :color="RatingData[rating]!.color" :size="props.size"/>
</template>

<script setup lang="ts">
import {useAdStrategyStore} from "../../ad/strategy/ad-strategy-store.ts";
import {computed} from "vue";

const strategyStore = useAdStrategyStore();
const props = defineProps({
  score: Number,
  size: String,
});

enum Rating {
  PENDING, BEIGE, RED, AMBER, GREEN
}

const RatingData: { [rating in Rating]?: { color: string, icon: string } } = {
  [Rating.BEIGE]: {color: 'beige', icon: 'sentiment_dissatisfied'},
  [Rating.RED]: {color: 'red', icon: 'sentiment_neutral'},
  [Rating.AMBER]: {color: 'amber', icon: 'sentiment_satisfied'},
  [Rating.GREEN]: {color: 'green', icon: 'sentiment_very_satisfied'},
}

const rating = computed(() => {
  if (strategyStore.data.fetching || props.score === undefined) {
    return Rating.PENDING;
  }
  const strategy = strategyStore.data.strategy;
  if (props.score == null) {
    return Rating.BEIGE;
  } else if (props.score >= strategy!.rating_high_min_score) {
    return Rating.GREEN;
  } else if (props.score >= strategy!.rating_medium_min_score) {
    return Rating.AMBER;
  } else {
    return Rating.RED;
  }
});
</script>

<style scoped>
.text-beige {
  color: #e1c699 !important;
}

.bg-beige {
  background: #e1c699 !important;
}
</style>