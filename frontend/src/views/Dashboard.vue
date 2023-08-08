<template>
    
    <v-container class="fill-height">
        <v-row style="background-color: white; border-radius: 15px;">
            <v-col cols="8" sm="8">
                <SecondComponent></SecondComponent>
            </v-col>
            <v-col cols="4" sm="4">
                <FirstComponent></FirstComponent>
            </v-col>
        </v-row>
    </v-container>
    <Footer></Footer>

</template>
  
<script lang="ts" setup>
    import { ref } from 'vue';
    import FirstComponent from '@/components/dashboard/FirstComponent.vue'
    import SecondComponent from '@/components/dashboard/SecondComponent.vue'
    import Footer from '@/components/Footer.vue'
</script>
<style>
.fill-height {
  height: 100vh;
}
</style>
  