<template>
  <v-container>
    <v-card v-if="isLogedIn">
      <v-card-title>Deine Daten:</v-card-title>
      <v-card-subtitle v-text="userInfo['name']"></v-card-subtitle>
      <v-card-text v-for="(value, key) in userInfo" :key="key">{{ key }}: {{ value }}</v-card-text>
      <v-btn class="justify-center text-center align-center ma-3" @click="getData">Get data from backend</v-btn>
      <v-card-text v-for="(value, key) in backendData" :key="key">
        <div v-if="error" class="errorStyle">{{ key }}: {{ value }}</div>
        <div v-else class="sucessStyle">{{ key }}: {{ value }}</div>
      </v-card-text>
    </v-card>
    <v-card v-else>
      <v-card-title>
        Nicht eingeloggt!
      </v-card-title>
      <v-card-subtitle>
        klicke rechts oben auf den Login button!
      </v-card-subtitle>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: 'HelloWorld',
  computed: {
    userInfo() {
      const userInfo = localStorage.getItem("userInfo");
      console.log('userInfo', userInfo);
      return JSON.parse(userInfo);
    },
    isLogedIn() {
      const token = localStorage.getItem("vue-token");
      const logedIn = token && token.length > 0 && token !== "null";
      return logedIn;
    },
    token() {
      return localStorage.getItem("vue-token");
    }
  },
  methods: {
    async getData() {
      await axios.create({
        baseURL: this.API_URL,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem("vue-token")
        }
      })
          .get("basic/test/")
          .then(res => {
            console.log(res);
            this.backendData = res.data;
            this.error = false;
          }).catch((error) => {
            console.log(error);
            this.backendData = error;
            this.error = true;
          });
    }
  },
  data: () => ({
    API_URL: 'http://localhost:8000/',
    backendData: {
      "content": "nocht nichts"
    },
    error: false
  }),
}
</script>

<style scoped>
.errorStyle {
  color: red;
}

.sucessStyle {
  color: green;
}
</style>
