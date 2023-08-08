<template>
    <v-container>
        <v-row justify="space-around">
            <v-card max-width="500" class="mx-auto">
                <v-container>
                    <v-row dense>
                        <v-col cols="12">
                            <v-card color="primary">
                                <v-card-title class="text-h5">
                                ¡No más filas!
                                </v-card-title>
                                <v-card-subtitle>Consigna el dinero a una de tus cuentas de inmediato</v-card-subtitle>
                                <v-card-actions>
                                    <v-btn variant="text" @click="topup">
                                        Consignar ahora
                                    </v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-col>
                        <v-col cols="12">
                        <v-card color="primary">
                            <v-card-title class="text-h5">
                            No pierdas el rastro...
                            </v-card-title>

                            <v-card-subtitle>Consulta el saldo de cualquiera de las cuentas</v-card-subtitle>

                            <v-card-actions>
                            <v-btn @click="check" variant="text">
                                Consultar saldo
                            </v-btn>
                            </v-card-actions>
                        </v-card>
                        </v-col>
                        <v-col cols="12">
                        <v-card color="#ff8100">
                            <v-card-title class="text-h5">
                            ¿Efectivo?
                            </v-card-title>

                            <v-card-subtitle>Solicita un retiro de cualquiera de las cuentas</v-card-subtitle>

                            <v-card-actions>
                            <v-btn @click="withdraw" variant="text">
                                Retirar ahora
                            </v-btn>
                            </v-card-actions>
                        </v-card>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card>
        </v-row>
    </v-container>
    <v-dialog v-model="addBalanceModal" persistent max-width="500">
      <v-card>
        <v-card-title>
          <span class="headline">Consignar a una cuenta</span>
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="addBalance">
            <v-select
                v-model="selectedAccount"
                :items="accounts"
                label="Seleccione una cuenta"
            ></v-select>
            <v-text-field 
                v-model="balance" 
                label="Ingrese el valor a consignar"
                pattern="[0-9]{0,10}"  
                @keypress="verifyBalance">
            </v-text-field>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="addBalanceModal = false">Cancelar</v-btn>
              <v-btn :disabled="isBalanceDisabled" color="primary" text type="submit">Consignar</v-btn>
            </v-card-actions>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="getBalanceModal" persistent max-width="500">
      <v-card>
        <v-card-title>
          <span class="headline">Consultar saldo de una cuenta</span>
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="getBalance">
            <v-select
                v-model="selectedAccountGetBalance"
                :items="accounts"
                label="Seleccione una cuenta"
            ></v-select>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="getBalanceModal = false">Cancelar</v-btn>
              <v-btn :disabled="isGetBalanceDisabled" color="primary" text type="submit">Consultar</v-btn>
            </v-card-actions>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="cashBalanceModal" persistent max-width="500">
      <v-card>
        <v-card-title>
          <span class="headline">Retirar de una cuenta</span>
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="removeBalance">
            <v-select
                v-model="selectedAccountCash"
                :items="accounts"
                label="Seleccione una cuenta"
            ></v-select>
            <v-text-field 
                v-model="cashBalance" 
                label="Ingrese el valor a retirar"
                pattern="[0-9]{0,10}"  
                @keypress="verifyBalance">
            </v-text-field>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click="cashBalanceModal = false">Cancelar</v-btn>
              <v-btn :disabled="isCashBalanceDisabled" color="primary" text type="submit">Retirar</v-btn>
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

import { defineComponent, ref, computed, getCurrentInstance } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';

export default defineComponent({
  setup() {
    const token = sessionStorage.getItem('token');
    const addBalanceModal = ref(false);
    const getBalanceModal = ref(false);
    const cashBalanceModal = ref(false);
    const selectedAccount = ref(null);
    const selectedAccountGetBalance = ref(null);
    const selectedAccountCash = ref(null);
    const resultModal = ref(false);
    const resultTitle = ref('');
    const resultMessage = ref('');
    const accounts = ref([]);
    const balance = ref('');
    const cashBalance = ref('');
    const store = useStore();

    const isBalanceDisabled = computed(() => {
        return (
            selectedAccount.value === null ||
            balance.value.trim() === ''
        );
    });

    const isGetBalanceDisabled = computed(() => {
        return (
            selectedAccountGetBalance.value === null
        );
    });

    const isCashBalanceDisabled = computed(() => {
        return (
            selectedAccountCash.value === null ||
            cashBalance.value.trim() === ''
        );
    });

    const getAccountsById = async () =>{
        const userData = {holder: store.getters.getUser.username}
        const response = await axios.post('get_accounts_by_id/', userData, {
            headers: {
                Authorization: 'Token ' + token,
            }, 
        });
        
        accounts.value = response.data.account_numbers
    }
    getAccountsById()

    const topup = () =>{
        addBalanceModal.value= true
        getAccountsById()
    }
    const check = () =>{
        getBalanceModal.value= true
        getAccountsById()
    }
    const withdraw = () =>{
        cashBalanceModal.value= true
        getAccountsById()
    }

    const addBalance = async () =>{
        const sendData = {
            account_number: selectedAccount.value,
            balance: balance.value,
            holder: store.getters.getUser.username
        }
        try{
            const response = await axios.post('add_balance/',sendData , {
                headers: {
                  Authorization: 'Token '+ token,
                },  
            })
            const { status, account, code, new_balance } = response.data;
            const formattedBalance = parseFloat(new_balance).toLocaleString('en-US', {
                style: 'currency',
                currency: 'USD'
            });
            if (status) {
                balance.value= ''
                selectedAccount.value = null
                addBalanceModal.value = false;
                resultTitle.value = 'Consignación satisfactoria';
                resultMessage.value = 'Se ha consignado a la cuenta '+account+'. Código de radicado: '+code+ '. Nuevo saldo: '+formattedBalance;
                resultModal.value = true;
            }
        }catch(error){
                addBalanceModal.value = false;
                resultTitle.value = 'Error';
                resultMessage.value = 'No se ha podido realizar la consignación, intente más tarde.';
                resultModal.value = true;
        }
    }

    const getBalance = async () =>{
        const sendData = {
            account_number: selectedAccountGetBalance.value,
        }
        try{
            const response = await axios.post('get_balance_by_account/',sendData , {
                headers: {
                  Authorization: 'Token '+ token,
                },  
            })
            const formattedBalance = parseFloat(response.data.balance).toLocaleString('en-US', {
                style: 'currency',
                currency: 'USD'
            });
            getBalanceModal.value = false;
            resultTitle.value = 'Consulta de saldo';
            resultMessage.value = 'La cuenta '+ selectedAccount.value + 'tiene un saldo de: '+formattedBalance;
            balance.value= ''
            selectedAccount.value = null
            resultModal.value = true;

        }catch(error){
                console.log(error)
                getBalanceModal.value = false;
                resultTitle.value = 'Error';
                resultMessage.value = 'No se ha podido realizar la consulta, intente más tarde.';
                resultModal.value = true;
        }
    }

    const removeBalance = async () =>{
        const sendData = {
            account_number: selectedAccountCash.value,
            balance: cashBalance.value,
            holder: store.getters.getUser.username
        }
        try{
            const response = await axios.post('subtract_balance/',sendData , {
                headers: {
                  Authorization: 'Token '+ token,
                },  
            })
            const { status, account, code, new_balance } = response.data;
            const formattedBalance = parseFloat(new_balance).toLocaleString('en-US', {
                style: 'currency',
                currency: 'USD'
            });
            if (status) {
                balance.value= ''
                selectedAccount.value = null
                addBalanceModal.value = false;
                resultTitle.value = 'Retiro satisfactorio';
                resultMessage.value = 'Se ha retirado de la cuenta '+account+'. Código de radicado: '+code+ '. Nuevo saldo: '+formattedBalance;
                resultModal.value = true;
            }
        }catch(error){
                const formattedErrorBalance = parseFloat(error.response.data.balance).toLocaleString('en-US', {
                    style: 'currency',
                    currency: 'USD'
                });
                if (error.response.data.status){
                    resultMessage.value = 'No hay saldo suficiente para realizar el retiro en esta cuenta.  Saldo actual '+ formattedErrorBalance;
                }else{
                    resultMessage.value = 'No se ha podido realizar el retiro, intente más tarde.';
                }
                resultTitle.value = 'Error';
                resultModal.value = true;
        }
    }

    const verifyBalance = (event: KeyboardEvent) => {
        if (event.key && (!/^[0-9]$/.test(event.key) || balance.value.length >= 10)) {
          event.preventDefault();
        }
    };

    return {
        addBalanceModal,
        getBalanceModal,
        cashBalanceModal,
        selectedAccount,
        selectedAccountGetBalance,
        selectedAccountCash,
        accounts,
        balance,
        cashBalance,
        isBalanceDisabled,
        isGetBalanceDisabled,
        isCashBalanceDisabled,
        resultModal,
        resultTitle,
        resultMessage,
        verifyBalance,
        addBalance,
        getBalance,
        removeBalance,
        topup,
        check,
        withdraw,
    };
  },
});
</script>
  