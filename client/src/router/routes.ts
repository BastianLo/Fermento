import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: 'RecipeManager',
        children: [
          {
            path: 'recipe',
            name: 'RecipeOverview',
            component: () =>
              import('pages/RecipeManager/recipeOverviewPage.vue'),
            children: [],
          },
          {
            path: 'recipe/:id',
            name: 'RecipeSingle',
            component: () =>
              import('pages/RecipeManager/recipeDetailsPage.vue'),
          },
        ],
      },
      {
        path: '',
        component: () => import('pages/IndexPage.vue'),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
