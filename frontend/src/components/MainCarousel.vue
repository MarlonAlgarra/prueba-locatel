<template>
  <v-carousel
    height="600"
    cycle
    hide-delimiter-background
    show-arrows="hover"
  >
    <v-carousel-item
      src="/src/assets/slide1.jpg"
      cover
    >
      <div class="d-flex fill-height justify-center align-center">
        <div class="background-text">
          <div class="text-h2" style="color: white;">
            <div style="justify-content: center; display: flex;">
              <strong>¡Empieza hoy!</strong>
            </div>
            <div style="justify-content: center; display: flex;">
              <strong>Crea tu cuenta de gestión</strong>
            </div>
            <v-btn to="/signup" block color="white" variant="tonal" prepend-icon="mdi-bank-plus">
                Crear cuenta
            </v-btn>
          </div>
        </div>
        
      </div>
    </v-carousel-item>
    <v-carousel-item
      src="/src/assets/slide2.jpg"
      cover
    >
      <div class="d-flex fill-height justify-center align-center">
        <div class="background-text">
          <div class="text-h2" style="color: white;">
            <div style="justify-content: center; display: flex;">
              <strong>No te sientas perdido</strong>
            </div>
            <div style="justify-content: center; display: flex;">
              <strong>¡Consulta tu saldo!</strong>
            </div>
            <v-btn  to="/login" block color="white" variant="tonal" prepend-icon="mdi-bank-plus">
                Consultar saldo
            </v-btn>
          </div>
        </div>
        
      </div>
    </v-carousel-item>
    <v-carousel-item
      src="/src/assets/slide4.jpg"
      cover
    >
      <div class="d-flex fill-height justify-center align-center">
        <div class="background-text">
          <div class="text-h2" style="color: white;">
            <div style="justify-content: center; display: flex;">
              <strong>¡Cuenta con nosotros!</strong>
            </div>
            <div style="justify-content: center; display: flex;">
              <strong>Realiza una consignación ahora</strong>
            </div>
            <v-btn to="/login" block color="white" variant="tonal" prepend-icon="mdi-bank-plus">
                Realizar consignación
            </v-btn>
          </div>
        </div>
        
      </div>
    </v-carousel-item>
  </v-carousel>
</template>
<script lang="ts">
  export default {
    data () {
      return {
        slides: [
          'Crea una cuenta de ahorros',
          'Consigna tu dinero fácilmente',
          'Retira tu dinero',
          'Consulta tu saldo',
        ],
      }
    },
  }
</script>
<style>
.background-text{
  background-color: rgb(129, 142, 133,.7);
  width: 60%;
  height: 40%;
  justify-content: center;
  display: flex;
  align-items: center;
}
</style>