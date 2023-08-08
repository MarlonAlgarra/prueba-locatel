<template>
  <v-app>
    <default-bar title="Sistema bancario"/>

    <default-view />
    <footer></footer>
  </v-app>
</template>

<script lang="ts" setup>
  import DefaultBar from './AppBar.vue'
  import DefaultView from './View.vue'
  import Footer from './Footer.vue'
</script>
