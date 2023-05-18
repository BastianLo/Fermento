import { defineStore } from 'pinia';
import axios from 'axios';

export const useRecipeStore = defineStore('recipe', {
  state: () => ({
    recipes: [],
  }),

  getters: {},

  actions: {
    async fetchRecipes() {
      try {
        const access_token = localStorage.getItem('access_token');
        const API_ENDPOINT = process.env.DEV ? 'http://127.0.0.1:8000' : '';
        const data = await axios.get(`${API_ENDPOINT}/api/recipe/`, {
          headers: {
            Authorization: `JWT ${access_token}`,
          },
        });
        this.recipes = data.data;
      } catch (error) {
        alert(error);
        console.log(error);
      }
    },
  },
});
