<template>
  <v-app-bar height="90" color="primary">
    <!-- <v-app-bar-nav-icon @click="toggleSidebar" /> -->
    <v-img
      class="mx-12"
      src="https://locatelcolombia.vtexassets.com/assets/vtex.file-manager-graphql/images/d24047f6-548e-44f2-9ef6-d0e6e48229f9___1bc6e809f887b47ea360ee4ade95fbcc.png"
      max-height="170"
      max-width="170"
      contain
      @click="redirectToBase"
    ></v-img>
    <v-toolbar-title style="color:white; font-size:30px">{{ title }}</v-toolbar-title>
    <v-btn to="/login" color="white" variant="outlined" style="margin-right: 1%;"  prepend-icon="mdi-account">
        Ingresar
    </v-btn>
    <v-btn to="/signup" color="white" variant="outlined" prepend-icon="mdi-bank-plus">
        Crear cuenta
    </v-btn>

  </v-app-bar>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
export default defineComponent({
  name: 'DefaultBar',
  props: {
    title: {
      type: String as PropType<string>,
      required: true,
    },
  },
  methods: {
    toggleSidebar() {
    },
    redirectToBase() {
      this.$router.push('/');
    },
  },
});
</script>

<style>
</style>

