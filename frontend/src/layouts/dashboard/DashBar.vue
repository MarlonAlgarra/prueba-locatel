<template>
        <v-app-bar height="90" color="primary">
        <v-app-bar-nav-icon variant="text" @click="drawer = !drawer"></v-app-bar-nav-icon>
        <v-img
          class="mx-12"
          src="https://locatelcolombia.vtexassets.com/assets/vtex.file-manager-graphql/images/d24047f6-548e-44f2-9ef6-d0e6e48229f9___1bc6e809f887b47ea360ee4ade95fbcc.png"
          max-height="170"
          max-width="170"
          contain
          @click="redirectToBase"
        ></v-img>
        <v-toolbar-title style="color:white; font-size:30px">Bienvenido al {{ title }}, {{ user.first_name }}</v-toolbar-title>
        <v-btn @click="logout" color="white" variant="outlined" style="margin-right: 1%;"  prepend-icon="mdi-logout">
            Cerrar sesión
        </v-btn>  
      </v-app-bar>
  
      <v-navigation-drawer
      expand-on-hover
      v-model="drawer"
        rail
      >
        <v-list density="compact" nav>
          <v-list-item @click="goDashboard" prepend-icon="mdi-home" title="Dashboard"></v-list-item>
          <v-list-item @click="activity" prepend-icon="mdi-history" title="Actividad"></v-list-item>
        </v-list>
      </v-navigation-drawer>
  </template>
  <script lang="ts">
  import { defineComponent, PropType, computed, ref } from 'vue';
  import { useStore } from 'vuex';
  import { useRouter } from 'vue-router';
  
  export default defineComponent({
    name: 'DashBar',
    props: {
      title: {
        type: String as PropType<string>,
        required: true,
      },
    },
    setup() {
      const store = useStore();
      const router = useRouter();
      const drawer = ref(false)
  
      const user = computed(() => {
          return store.getters.getUser;
      });
  
      const logout = () => {
        store.dispatch('logout');
        router.push('/')
      };
  
      const goDashboard = () => {
        router.push('/dashboard');
      };

      const activity = () => {
        router.push('/dashboard/activity');
      };
      const redirectToBase = () => {
        router.push('/dashboard');
      };

      return {
        user,
        logout,
        redirectToBase,
        drawer,
        goDashboard,
        activity
      };
    },
  });
  </script>
