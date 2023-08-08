<template>
    <v-row>
        <v-col cols="6" sm="6">
            <h1>Actividad del usuario</h1>
        </v-col>
        <v-col cols="6" sm="6" align="end">
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
  </template>
<script lang="ts">

import { defineComponent, ref, computed} from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';

export default defineComponent({
  setup() {
    const token = sessionStorage.getItem('token');
    const store = useStore();
    const accountData = ref([]);

    const user = computed(() => {
        return store.getters.getUser;
    });

    const getActivity = async () =>{
        const userData = {holder: store.getters.getUser.username}
        const response = await axios.post('get_activity_by_user/', userData, {
            headers: {
                Authorization: 'Token ' + token,
            }, 
        });
        const formattedAccounts = response.data.map(account => {
            const formattedBalance = parseFloat(account.value).toLocaleString('en-US', {
                style: 'currency',
                currency: 'USD'
            });

            return {
                ...account,
                value: formattedBalance,
            };
        });
        accountData.value = formattedAccounts
    }
    getActivity()

    const updateTable = () =>{
        accountData.value = []
        getActivity()
    }

    return {
      itemsPerPage: 10,
      headers: [
        {title: 'Tipo de evento', align: 'start', key: 'transactionType'},
        { title: 'Fecha y hora', align: 'start', key: 'date_time'},
        { title: 'Valor', align: 'start', key: 'value' },
        { title: 'Cuenta', align: 'start', key: 'account_number' },
        { title: 'Codigo de transacción', align: 'end', key: 'track_id' },
      ],
      document,
      accountData,
      updateTable
    };
  },
});
</script>