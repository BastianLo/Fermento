<template>
  <p>abc</p>
  <p>Recipe ID: {{ id }}</p>
</template>

<script setup>
import { useRecipeStore } from 'stores/recipe';
import { useRoute } from 'vue-router';

const route = useRoute();
const id = route.params.id;

const store = useRecipeStore();

store.fetchRecipes();
</script>

<style scoped>
.recipe-image {
  height: 200px; /* set a fixed height */
  object-fit: cover; /* maintain aspect ratio and fill container */
}
</style>
