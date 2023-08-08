<template>
    <v-container class="fill-height" fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card>
            <v-card-title class="text-center">
              <h2>Iniciar sesión</h2>
            </v-card-title>
            <v-card-text>
              <v-form @submit.prevent="login">
                <v-text-field
                  v-model="username"
                  label="Ingrese el número de cédula"
                  type="text"
                  outlined
                  required
                  pattern="[0-9]{0,10}"  
                  @keypress="verifyValue"
                ></v-text-field>
                <v-text-field
                  v-model="password"
                  label="Ingrese la contraseña"
                  :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showPassword ? 'text' : 'password'"
                  @click:append="togglePasswordVisibility"
                  outlined
                  required
                ></v-text-field>
                <v-btn :disabled="isLoginButtonDisabled" type="submit" color="#01962D" block><p style="color: white;">Ingresar</p></v-btn>
              </v-form>

              <v-dialog v-model="loading" :scrim="false" persistent width="auto">
                <v-card color="#01962D">
                    <v-card-text style="color:white;">
                    Verificando...
                    <v-progress-linear
                        indeterminate
                        color="white"
                        class="mb-0"
                    ></v-progress-linear>
                    </v-card-text>
                </v-card>
              </v-dialog>

              <v-dialog v-model="errorModal" width="auto">
                <v-card>
                    <v-card-title>Error</v-card-title>
                    <v-card-text>
                        {{ errorMessage }}
                    </v-card-text>
                    <v-card-actions>
                    <v-btn color="primary" @click="errorModal = false">Aceptar</v-btn>
                    </v-card-actions>
                </v-card>
              </v-dialog>

            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
</template>
  
  <script lang="ts">
  import { defineComponent, ref, computed} from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import { useStore } from 'vuex';
  
  export default defineComponent({
    setup() {
      const username = ref('');
      const password = ref('');
      const loading = ref(false)
      const errorModal = ref(false);
      const errorMessage = ref('');
      const showPassword = ref(false);
      const store = useStore();
      const router = useRouter();
  
      if(localStorage.getItem('tempUser')){
        username.value = localStorage.getItem('tempUser')
        localStorage.removeItem("tempUser");
      }

      const isLoginButtonDisabled = computed(() => {
        return username.value.trim() === '' || password.value.trim() === '';
      });
      const togglePasswordVisibility = () => {
        showPassword.value = !showPassword.value;
      };
  
      const login = async () => {
        loading.value = true;
        setTimeout(() => (loading.value = false), 3000)
        try {
          const response = await axios.post('login/', {
            username: username.value,
            password: password.value,
          });
  
          const { status, data } = response.data;
          if (status) {
            sessionStorage.setItem('token', data.token);
            store.dispatch('login')
            store.dispatch('setUser', data);
            loading.value = false;
            router.push('/dashboard');
          }
        } catch (error) {
          console.error('Error al hacer login:', error.response.data);
          loading.value = false;
          errorMessage.value = 'Ha ocurrido un error en el inicio de sesión. Por favor, verifique sus credenciales e intente nuevamente.';
          errorModal.value = true;
        }
      };
  
      const verifyValue = (event: KeyboardEvent) => {
        if (event.key && (!/^[0-9]$/.test(event.key) || username.value.length >= 10)) {
          event.preventDefault();
        }
      };
  
      return {
        username,
        password,
        isLoginButtonDisabled,
        loading,
        errorModal,
        errorMessage,
        showPassword,
        togglePasswordVisibility,
        login,
        verifyValue,
      };
    },
  });
  </script>
  <style>
  .fill-height {
    height: 100vh;
  }
  </style>
  