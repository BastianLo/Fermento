<template>
  <div class="q-pa-md row items-start q-gutter-md">
    <q-card
      v-for="product in store.recipes"
      :key="product.id"
      class="my-card"
      flat
      bordered
    >
      <q-img :src="product.image" class="recipe-image" />

      <q-card-section>
        <q-btn
          fab
          color="primary"
          icon="place"
          class="absolute"
          style="top: 0; right: 12px; transform: translateY(-50%)"
        />

        <div class="row no-wrap items-center">
          <div class="col text-h6 ellipsis" v-text="product.name"></div>
          <div
            class="col-auto text-grey text-caption q-pt-md row no-wrap items-center"
          >
            <q-icon name="place" />
            250 ft
          </div>
        </div>

        <q-rating v-model="stars" :max="5" size="32px" />
      </q-card-section>

      <q-card-section class="q-pt-none">
        <div class="text-subtitle1">$・Italian, Cafe</div>
        <div class="text-caption text-grey">
          Small plates, salads & sandwiches in an intimate setting.
        </div>
      </q-card-section>

      <q-separator />

      <q-card-actions>
        <q-btn flat round icon="event" />
        <q-btn flat color="primary"> Reserve</q-btn>
      </q-card-actions>
    </q-card>
  </div>
</template>

<script setup>
import { useRecipeStore } from 'stores/recipe';

const store = useRecipeStore();

store.fetchRecipes();
</script>

<style scoped>
.recipe-image {
  height: 200px; /* set a fixed height */
  object-fit: cover; /* maintain aspect ratio and fill container */
}
</style>
