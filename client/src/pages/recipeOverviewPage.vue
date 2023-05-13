<template>
  <div class="q-pa-md row items-start q-gutter-md">
    <q-card
      style="width: 300px"
      v-for="product in store.recipes"
      :key="product.id"
      class="my-card"
      flat
      bordered
    >
      <q-img :src="product.image" class="recipe-image" />

      <q-card-section>
        <div class="row no-wrap items-center">
          <div class="col text-h6 ellipsis" v-text="product.name"></div>
          <q-badge
            rounded
            :color="
              product.difficulty === 'easy'
                ? 'green'
                : product.difficulty === 'medium'
                ? 'orange'
                : 'red'
            "
            :label="product.difficulty"
          />
          <div
            class="col-auto text-grey text-caption q-pt-md row no-wrap items-center"
          ></div>
        </div>

        <q-rating readonly v-model="product.rating" :max="5" size="32px" />
      </q-card-section>

      <q-card-section class="q-pt-none">
        <div
          v-text="product.description.toString().substring(0, 50)"
          class="text-caption text-grey"
        ></div>
      </q-card-section>
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
