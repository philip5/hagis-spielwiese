<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <div class="d-flex align-center">
        <v-img
            alt="Vuetify Logo"
            class="shrink mr-2"
            contain
            src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
            transition="scale-transition"
            width="40"
        />

        <v-img
            alt="Vuetify Name"
            class="shrink mt-1 hidden-sm-and-down"
            contain
            min-width="100"
            src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
            width="100"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn text v-if="!isLogedIn" @click="login">
        <span class="mr-2">Login beim IDM</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
      <v-btn text v-else @click="logout">
        <span class="mr-2">Logout</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

import Keycloak from "keycloak-js";

export default {
  name: 'App',
  computed: {
    isLogedIn() {
      const token = localStorage.getItem("vue-token");
      const logedIn = token && token.length > 0 && token !== "null";
      return logedIn;
    },
  },
  data: () => ({
    initOptions: {
      url: 'https://auth.anmelde-tool.de/auth',
      realm: 'Hagis-Spielwiese',
      clientId: 'localhost',
      onLoad: 'check-sso',
      checkLoginIframe: false,
    },
    API_URL: "localhost:8000"
  }),
  methods: {
    login() {
      this.keycloak.login().then((auth) => {
        if (auth) {
          console.log("Authenticated");
          localStorage.setItem("vue-token", this.keycloak.token);
          localStorage.setItem("vue-refresh-token", this.keycloak.refreshToken);
          this.keycloak.loadUserInfo().then(userInfo => {
            localStorage.setItem('userInfo', JSON.stringify(userInfo));
          });
        }
      }).catch((error) => {
        console.error("Authenticated Failed: ", error);
        localStorage.setItem("vue-token", null);
        localStorage.setItem("vue-refresh-token", null);
      });
      this.refreshToken();
    },
    logout() {
      this.keycloak.logout();
      localStorage.setItem("vue-token", null);
      localStorage.setItem("vue-refresh-token", null);
      localStorage.setItem('userInfo', null);
    },
    refreshToken() {
      if (this.isLogedIn) {
        setInterval(() => {
          this.keycloak.updateToken(70).then((refreshed) => {
            if (refreshed) {
              console.log('Token refreshed' + refreshed);
            } else {
              console.log('Token not refreshed, valid for '
                  + Math.round(this.keycloak.tokenParsed.exp + this.keycloak.timeSkew - new Date().getTime() / 1000) + ' seconds');
            }
          }).catch(() => {
            console.log('Failed to refresh token');
          });
        }, 6000);
      }
    }
  },
  mounted() {
    this.keycloak = Keycloak(this.initOptions);

    this.keycloak.init({
      onLoad: this.initOptions.onLoad,
      checkLoginIframe: this.initOptions.checkLoginIframe
    }).then((auth) => {
      if (auth) {
        console.log("Authenticated");
        localStorage.setItem("vue-token", this.keycloak.token);
        localStorage.setItem("vue-refresh-token", this.keycloak.refreshToken);
        this.keycloak.loadUserInfo().then(userInfo => {
          localStorage.setItem('userInfo', JSON.stringify(userInfo));
        });
      }
    }).catch((error) => {
      console.error("Authenticated Failed: ", error);
    });
    this.refreshToken();
  }
};
</script>
