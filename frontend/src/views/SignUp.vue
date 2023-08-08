<template>
    <v-container class="fill-height" fluid>
      <v-row align="center" justify="center">
        <v-col cols="12" sm="8" md="4">
          <v-card>
            <v-card-title class="text-center">
              <h2>Crear cuenta de gestión</h2>
            </v-card-title>
            <v-card-text>
                <v-form @submit.prevent="createUser">
                    <v-container>
                    <v-row>
                        <v-col cols="6">
                        <v-text-field v-model="firstName" label="Nombre"></v-text-field>
                        </v-col>
                        <v-col cols="6">
                        <v-text-field v-model="lastName" label="Apellido"></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="12">
                        <v-text-field 
                            v-model="username" 
                            label="Número de cédula" 
                            pattern="[0-9]{0,10}"  
                            @keypress="verifyValue"
                        ></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="12">
                        <v-text-field v-model="email" label="Correo electrónico" type="email" :rules="emailRules"></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field 
                             v-model="password" 
                             label="Contraseña" 
                             :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                             :type="showPassword ? 'text' : 'password'"
                             @click:append="togglePasswordVisibility" 
                             :rules="passwordRules">
                            </v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field v-model="confirmPassword" label="Confirmar contraseña" type="password" :rules="confirmPasswordRules"></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="12">
                        <v-btn @click="createUser" :disabled="isButtonDisabled" color="#01962D" block><p style="color: white;">Crear usuario</p></v-btn>
                        </v-col>
                    </v-row>
                    </v-container>
                </v-form>
                <v-dialog v-model="loading" :scrim="false" persistent width="auto">
                <v-card color="#01962D">
                    <v-card-text style="color:white;">
                    Creando...
                    <v-progress-linear
                        indeterminate
                        color="white"
                        class="mb-0"
                    ></v-progress-linear>
                    </v-card-text>
                </v-card>
              </v-dialog>

              <v-dialog v-model="errorModal" width="auto" persistent>
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
              <v-dialog v-model="successModal" width="auto" persistent>
                <v-card>
                    <v-card-title>¡Listo!</v-card-title>
                    <v-card-text>
                        {{ successMessage }}
                    </v-card-text>
                    <v-card-actions>
                    <v-btn color="primary" @click="redirectToLogin">Aceptar</v-btn>
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
  import { defineComponent, ref, computed } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';

  export default defineComponent({
    setup() {
      const firstName = ref('');
      const lastName = ref('');
      const username = ref('');
      const email = ref('');
      const password = ref('');
      const confirmPassword = ref('');
      const loading = ref(false)
      const errorModal = ref(false);
      const errorMessage = ref('');
      const successModal = ref(false);
      const successMessage = ref('');
      const showPassword = ref(false);
      const router = useRouter();
  
      const isButtonDisabled = computed(() => {
        return (
          firstName.value.trim() === '' ||
          lastName.value.trim() === '' ||
          username.value.trim() === '' ||
          password.value.trim() === '' ||
          confirmPassword.value.trim() === '' ||
          password.value !== confirmPassword.value
        );
      });
  
      const togglePasswordVisibility = () => {
        showPassword.value = !showPassword.value;
      }

      const verifyValue = (event: KeyboardEvent) => {
        if (event.key && (!/^[0-9]$/.test(event.key) || username.value.length >= 10)) {
          event.preventDefault();
        }
      };

      const passwordRules = [
        (v) => !!v || 'La contraseña es requerida',
        (v) => v && v.length >= 8 || 'La contraseña debe tener al menos 8 caracteres',
      ];

      const confirmPasswordRules = [
          (v) => !!v || 'Confirmar contraseña es requerido',
          (v) => v === password.value || 'Las contraseñas no coinciden',
      ];

      const emailRules = [
          (v) => !!v || 'El correo electrónico es requerido',
          (v) => /.+@.+\..+/.test(v) || 'El correo electrónico debe tener un formato válido',
      ];

      const redirectToLogin = () =>{
        router.push('/login')
      }

      const createUser = async () => {
        if (password.value !== confirmPassword.value) {
          console.error('Las contraseñas no coinciden');
          return;
        }
        loading.value = true;
        setTimeout(() => (loading.value = false), 3000)
        const userData = {
            "username": username.value,
            "is_active": true,
            "is_staff": false,
            "first_name": firstName.value,
            "last_name": lastName.value,
            "password": password.value,
            "email" : email.value
        };
        try {
          const response = await axios.post('users/', userData);
  
          const { status, data } = response.data;
          if (status) {
            successMessage.value = 'Usuario creado exitosamente. Ingrese con sus credenciales.';
            successModal.value = true;
            loading.value = false;
            localStorage.setItem('tempUser',data.username)
          }
        } catch (error) {
          console.error('Error al crear el usuario:', error.response.data);
          loading.value = false;
          errorMessage.value = 'Ha ocurrido un error al crear el usuario. Por favor, verifique los campos e intente nuevamente.';
          errorModal.value = true;
        }
      };
  
      return {
        firstName,
        lastName,
        username,
        email,
        password,
        confirmPassword,
        isButtonDisabled,
        emailRules,
        passwordRules,
        confirmPasswordRules,
        loading,
        errorModal,
        errorMessage,
        successModal,
        successMessage,
        showPassword,
        togglePasswordVisibility,
        createUser,
        redirectToLogin,
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
  