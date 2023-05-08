<template>
  <div class="q-pa-md">
    <q-btn-dropdown :label="store.username" icon="person">
      <div class="row no-wrap q-pa-md">
        <div class="column items-center">
          <div v-if="store.username !== ''">
            <q-avatar size="72px">
              <img src="https://cdn.quasar.dev/img/boy-avatar.png" />
            </q-avatar>
            <div
              v-text="store.username"
              class="text-subtitle1 q-mt-md q-mb-xs"
            ></div>
            <q-btn
              color="primary"
              :label="$t('auth.logout')"
              push
              @click="store.logout()"
              size="sm"
              v-close-popup
            />
          </div>
          <div v-else>
            <q-card-section>
              <div class="text-h3">Login</div>
            </q-card-section>
            <q-card-section class="q-pt-none">
              <q-input
                :placeholder="$t('auth.username')"
                dense
                v-model="username"
                autofocus
              />
            </q-card-section>
            <q-card-section class="q-pt-none">
              <q-input
                :placeholder="$t('auth.password')"
                type="password"
                dense
                v-model="password"
                autofocus
              />
            </q-card-section>

            <q-card-actions align="right" class="text-primary">
              <q-btn flat :label="$t('common.button.cancel')" v-close-popup />
              <q-btn
                @click="store.login(username, password)"
                flat
                :label="$t('auth.login')"
                v-close-popup
              />
            </q-card-actions>
          </div>
        </div>
      </div>
    </q-btn-dropdown>
  </div>
</template>

<script setup>
import { useCounterStore } from 'stores/authentification';
import { ref } from 'vue';

const store = useCounterStore();

store.checkLogin();

let username = ref('');
let password = ref('');
</script>
