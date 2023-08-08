<template>
    <v-footer class="d-flex flex-column" style="width: 100%;">
      <div class="bg-primary d-flex w-100 align-center px-4" style="width: 100%;">
        <strong>Sistema desarrollado por Locatel</strong>
  
        <v-spacer></v-spacer>
  
        <v-btn
          v-for="icon in icons"
          :key="icon"
          class="mx-4"
          :icon="icon"
          variant="plain"
          size="small"
        ></v-btn>
      </div>
  
      <div class="px-4 py-2 bg-black text-center w-100">
        {{ new Date().getFullYear() }} — <strong>Locatel</strong>
      </div>
    </v-footer>
</template>
<script>
  export default {
    data: () => ({
      icons: [
        'mdi-linkedin',
      ],
    }),
  }
</script>