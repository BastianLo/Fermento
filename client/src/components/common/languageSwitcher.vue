<template>
  <!-- ...... -->
  <q-select
    v-model="locale"
    :options="localeOptions"
    :label="$t('language')"
    @update:model-value="changeLanguage"
    dense
    borderless
    emit-value
    map-options
    options-dense
    style="min-width: 150px"
  />
  <!-- ...... -->
</template>

<script>
import { useI18n } from 'vue-i18n';
import { Quasar, useQuasar } from 'quasar';

Quasar.lang.getLocale(); // returns a string

export default {
  setup() {
    const { locale } = useI18n({ useScope: 'global' });
    const $q = useQuasar();
    //locale.value = $q.lang.getLocale();
    locale.value = localStorage.getItem('selectedLanguage') || locale.value;

    const changeLanguage = () => {
      localStorage.setItem('selectedLanguage', locale.value);
    };
    return {
      locale,
      changeLanguage,
      localeOptions: [
        { value: 'en-US', label: 'English' },
        { value: 'de', label: 'Deutsch' },
      ],
    };
  },
};
</script>
