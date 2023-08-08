<template>
    
    <v-container class="fill-height">
        <v-row style="background-color: white; border-radius: 15px;">
            <v-col cols="12" sm="12">
                <history></history>
            </v-col>
        </v-row>
    </v-container>
    <Footer></Footer>

</template>
  
<script lang="ts" setup>
    import { ref } from 'vue';
    import history from '@/components/dashboard/history.vue'
    import Footer from '@/components/Footer.vue'
</script>
<style>
.fill-height {
  height: 100vh;
}
</style>
  