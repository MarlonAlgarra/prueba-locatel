<template>
    <v-row>
        <v-col cols="6" sm="6">
            <h1>Cuentas de ahorros creadas</h1>
        </v-col>
        <v-col cols="3" sm="3" align="end">
            <v-btn @click='errorModal = true' color="#01962D" variant="tonal" prepend-icon="mdi-bank-plus">
                Agregar cuenta
            </v-btn>
        </v-col>
        <v-col cols="3" sm="3" align="end">
            <v-btn @click='updateTable' color="#01962D" variant="tonal" prepend-icon="mdi-refresh">
                Actualizar tabla
            </v-btn>
        </v-col>

    </v-row>
    <v-row>
        <v-col cols="12" sm="12">
            <v-data-table
                v-model:items-per-page="itemsPerPage"
                :headers="headers"
                :items="accountData"
                item-value="name"
                class="elevation-1"
            ></v-data-table>
        </v-col>

    </v-row>

    <v-dialog v-model="errorModal" persistent max-width="500">
      <v-card>
        <v-card-title>
          <span class="headline">Agregar nueva cuenta de ahorros</span>
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="createAccount">
            <v-select
                v-model="selectedBank"
                :items="banks"
                label="Selecciona un banco"
            ></v-select>
            <v-text-field v-model="name" label="Nombre del propietario"></v-text-field>
            <v-text-field 
                v-model="document" 
                label="Documento de la persona"
                pattern="[0-9]{0,10}"  
                @keypress="verifyDocument">
            </v-text-field>
            <v-text-field 
                v-model="balance" 
                label="Valor inicial de la cuenta"
                pattern="[0-9]{0,10}"  
                @keypress="verifyBalance">
            </v-text-field>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="errorModal = false">Cancelar</v-btn>
              <v-btn :disabled="isButtonDisabled" color="primary" text type="submit">Guardar</v-btn>
            </v-card-actions>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="resultModal" width="auto">
        <v-card>
            <v-card-title>{{ resultTitle }}</v-card-title>
            <v-card-text>
                {{ resultMessage }}
            </v-card-text>
            <v-card-actions>
            <v-btn color="primary" @click="resultModal = false">Aceptar</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
  </template>
<script lang="ts">

import { defineComponent, ref, computed,  onMounted, onUnmounted } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';

export default defineComponent({
  setup() {
    const accountNumber = ref('');
    const selectedBank = ref(null);
    const owner = ref('');
    const ownerDocument = ref('');
    const name = ref('')
    const document = ref('')
    const balance = ref('')
    const errorModal = ref(false);
    const resultModal = ref(false);
    const resultTitle = ref('');
    const resultMessage = ref('');
    const token = sessionStorage.getItem('token');
    const banks = ref([]);
    const infoBanks = ref([]);
    const store = useStore();
    const accountData = ref([]);

    const user = computed(() => {
        return store.getters.getUser;
    });

    const isButtonDisabled = computed(() => {
        return (
          selectedBank.value === null ||
          name.value.trim() === '' ||
          document.value.trim() === '' ||
          balance.value.trim() === ''
        );
      });

    const getInfoBanks = async () => {
        const response = await axios.get('banks/', {
            headers: {
              Authorization: 'Token '+ token,
            },
        })
        infoBanks.value = response.data
        response.data.forEach(element=>{
            banks.value.push(element.name)
        })

    }
    getInfoBanks()

    const getAccounts = async () =>{
        const userData = {username: store.getters.getUser.username}
        const response = await axios.post('get_accounts/', userData, {
            headers: {
                Authorization: 'Token ' + token,
            }, 
        });
        const bankMapping = {};
        infoBanks.value.forEach(bank => {
            bankMapping[bank.id] = bank.name;
        });
        const formattedAccounts = response.data.map(account => {
            const formattedBalance = parseFloat(account.balance).toLocaleString('en-US', {
                style: 'currency',
                currency: 'USD'
            });

            return {
                ...account,
                balance: formattedBalance,
                bank: bankMapping[account.bank] || "Desconocido"
            };
        });
        accountData.value = formattedAccounts
    }
    getAccounts()

    const updateTable = () =>{
        accountData.value = []
        getAccounts()
    }

    const createAccount = async () => {
        const bankCode = infoBanks.value.find(bank => bank.name === selectedBank.value).code
        const bankId = infoBanks.value.find(bank => bank.name === selectedBank.value).id
        const assingNumber = `${new Date().getFullYear()}${(new Date().getUTCHours() + '').padStart(2, '0')}${(Math.floor(Math.random() * 10000) + '').padStart(4, '0')}`;
        const dataAccount = {
            account_number: bankCode+assingNumber,
            owner: name.value,
            owner_document: document.value,
            holder: store.getters.getUser.username,
            bank: bankId,
            balance: balance.value
        }
        try{
            const response = await axios.post('accounts/',dataAccount , {
                headers: {
                  Authorization: 'Token '+ token,
                },  
            })
            const { status, data } = response.data;
            if (status) {
                errorModal.value = false;
                resultTitle.value = 'Creacion satisfactoria';
                resultMessage.value = 'La cuenta ha sido creada correctamente. Observe los detalles en la tabla';
                resultModal.value = true;
                accountData.value = []
                getAccounts()
            }
        }catch(error){
            errorModal.value = false;
                resultTitle.value = 'Error';
                resultMessage.value = 'Ha ocurrido un error creando la cuenta. Intente más tarde';
                resultModal.value = true;
        }
    }

    const verifyBalance = (event: KeyboardEvent) => {
        if (event.key && (!/^[0-9]$/.test(event.key) || balance.value.length >= 10)) {
          event.preventDefault();
        }
    };
    const verifyDocument = (event: KeyboardEvent) => {
        if (event.key && (!/^[0-9]$/.test(event.key) || document.value.length >= 10)) {
          event.preventDefault();
        }
    };

    return {
      accountNumber,
      owner,
      ownerDocument,
      createAccount,
      itemsPerPage: 5,
      headers: [
        {
          title: 'Propietario de la cuenta',
          align: 'start',
          sortable: false,
          key: 'owner',
        },
        { title: 'Documento', align: 'start', key: 'owner_document'},
        { title: 'Número de cuenta', align: 'start', key: 'account_number' },
        { title: 'Banco', align: 'start', key: 'bank' },
        { title: 'Saldo', align: 'end', key: 'balance' },
      ],

      errorModal,
      selectedBank,
      banks,
      createAccount,
      name,
      document,
      balance,
      isButtonDisabled,
      verifyBalance,
      verifyDocument,
      resultModal,
      resultTitle,
      resultMessage,
      accountData,
      updateTable
    };
  },
});
</script>