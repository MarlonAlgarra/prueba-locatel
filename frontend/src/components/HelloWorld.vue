<template>
  <v-container>
    <v-responsive class="align-center text-center fill-height">
      <v-img height="200" src="@/assets/locatelLogo.png" />

      <div class="text-h4 font-weight-bold">Bienvenido al nuevo sistema de gestión bancario</div>

      <div class="text-h5 font-weight-light mb-n1 mt-2">Descubre cómo nuestras innovadoras soluciones simplifican tus operaciones financieras y te brindan un mayor control sobre tus transacciones.</div>
    </v-responsive>
  </v-container>
</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import { RouterLink } from 'vue-router';
  export default defineComponent({
  methods: {
  },
  components: {
    'router-link': RouterLink, 
  },
});
</script>
