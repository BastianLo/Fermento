import { defineStore } from 'pinia';
import axios from 'axios';

import { Notify } from 'quasar';

export const useCounterStore = defineStore('counter', {
  state: () => ({
    username: '',
    isLoggedIn: false,
    accessToken: null,
  }),

  getters: {},

  actions: {
    async login(username: string, password: string) {
      console.log('login');
      try {
        const API_ENDPOINT = process.env.DEV ? 'http://127.0.0.1:8000' : '';
        const response = await axios.post(`${API_ENDPOINT}/api/auth/login/`, {
          username: username,
          password: password,
        });
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('refresh_token', response.data.refresh);
        localStorage.setItem('username', username);
        this.checkLogin();
      } catch (error) {
        Notify.create({
          type: 'negative',
          message: 'Login failed',
        });
        console.error(error);
      }
    },
    logout() {
      console.log('logout');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      this.username = '';
    },
    checkLogin() {
      const accessToken = localStorage.getItem('access_token');
      const username = localStorage.getItem('username');
      if (accessToken) {
        this.accessToken = accessToken;
        this.isLoggedIn = true;
        this.username = username;
      }
    },
  },
});
