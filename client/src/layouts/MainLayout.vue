<template>
  <q-layout view="hHh lpR fFf" class="bg-grey-1">
    <q-header elevated class="bg-white text-grey-8 q-py-xs" height-hint="58">
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          @click="toggleLeftDrawer"
          aria-label="Menu"
          icon="menu"
        />

        <q-btn flat no-caps no-wrap class="q-ml-xs" v-if="$q.screen.gt.xs">
          <q-icon class="text-dark" size="28px">
            <q-img src="~assets/fermentation.png" />
          </q-icon>

          <q-toolbar-title class="text-weight-bold"> Fermento</q-toolbar-title>
        </q-btn>

        <q-space />

        <q-space />

        <div class="q-gutter-sm row items-center no-wrap">
          <language-switcher></language-switcher>
          <login-icon></login-icon>
        </div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      class="bg-grey-2"
      :width="240"
    >
      <q-scroll-area class="fit">
        <q-list padding>
          <q-item
            v-for="link in links1"
            :key="link.text"
            @click="router.push(link.location)"
            v-ripple
            clickable
          >
            <q-item-section avatar>
              <q-icon color="grey" :name="link.icon" />
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ link.text }}</q-item-label>
            </q-item-section>
          </q-item>

          <q-separator class="q-my-md" />

          <q-item v-for="link in links2" :key="link.text" v-ripple clickable>
            <q-item-section avatar>
              <q-icon color="grey" :name="link.icon" />
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ link.text }}</q-item-label>
            </q-item-section>
          </q-item>

          <q-separator class="q-mt-md q-mb-lg" />
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import LanguageSwitcher from 'components/common/languageSwitcher.vue';
import LoginIcon from 'components/common/loginIcon.vue';
import { useRouter } from 'vue-router';

import { useI18n } from 'vue-i18n';

const { t } = useI18n({ useScope: 'global' });
const router = useRouter();

let leftDrawerOpen = ref(false);
let links1 = ref([
  { icon: 'home', text: t('common.homepage'), location: '/' },
  {
    icon: 'restaurant_menu',
    text: t('recipe.label'),
    location: '/RecipeManager/recipe',
  },
  { icon: 'subscriptions', text: 'Subscriptions', location: '' },
]);
let links2 = ref([
  { icon: 'folder', text: 'Library', location: '' },
  { icon: 'restore', text: 'History', location: '' },
  { icon: 'watch_later', text: 'Watch later', location: '' },
  { icon: 'thumb_up_alt', text: 'Liked videos', location: '' },
]);

function toggleLeftDrawer() {
  leftDrawerOpen.value = !leftDrawerOpen.value;
}
</script>
