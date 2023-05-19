<template>
  <ft-container>
    <template #title>
      <span class="ft-d-flex">
        <label> Experiments Database</label>
        <label @click="showModal.config=true" class="ft-hover-text ft-pl-2"><font-awesome-icon :icon="['fas', 'gear']" /></label>
        <label @click="downloadData" class="ft-hover-text ft-pl-2"><font-awesome-icon :icon="['fas', 'file-csv']" /></label>
      </span>
      <span class="ft-d-flex ft-pt-2" style="width:250px;">
        <v-select
          class="ft-w-100" 
            v-if="loadOptions"
            v-model:modelValue="loadValue"
            :options="loadOptions">
            <template #no-options="{ search, searching, loading }">
                No Data Setting Created
            </template>
        </v-select>
        <button @click="loadSetting" class="ft-btn ft-border ft-btn-light ft-hover-text-white ft-hover-bg-ft "> Load</button>
      </span>
    </template>
    <div v-if="res.rows">
      <easy-data-table
        @click-row="showRow"
        @newSpec="setNewSpec"
        :headers="res.columns"
        :items="res.rows"
        buttons-pagination
        alternating="true"
        table-class-name="customize-table"
        header-text-direction="center"
        body-text-direction="center"
      />
    </div>
    <div>
      <row-data-modal 
        v-if="showModal.rowData" 
        @close="showModal.rowData=false"
        :selectedRow="selectedRow"
        :selectedRowData="selectedRowData"
      >
      </row-data-modal>
      <config-modal 
        v-if="showModal.config"
        @close="showModal.config=false"
        v-model:intialTableSpec="tableSpec"
        @update:intialTableSpec="loadTable"
      >
      </config-modal>
    </div>
    <div  class="home-div ft-pt-2 ft-pl-2" v-if="error">
      Server Error: {{JSON.stringify(res)}}
    </div>
    <div class="home-div ft-pt-2 ft-pl-2" v-if="success && !res">
        No Experiments Found
    </div>
  </ft-container>
</template>
  
<script>
  import FtContainer from '@/components/utils/ft-container/FtContainer.vue';
  import Vue3EasyDataTable from 'vue3-easy-data-table';
  import RowDataModal from '../components/structures/home-modals/RowDataModal.vue';
  import ConfigModal from '../components/structures/home-modals/ConfigModal.vue';
  import { downloadCSV } from '../utils/downloadCSV'; 

  const defaultTableSpec = {
    'exp_ids': [],
    "get_params": true,
    "get_metrics": true,
    "show": [
      'ix', 'exp_id', 'exp_name', 'exp_created', 'run_id', 'run_name', 'run_start', 'run_end'
    ],
    "rename": {
      'ix': 'Index',
      'exp_id': 'Emperiment Id',
      'exp_name': 'Experiment Name',
      'exp_created': 'Experiment Created',
      'run_id': 'Run Id',
      'run_name': 'Run Name',
      'run_start': 'Run Start',
      'run_end': 'Run End'
    }
  }
  export default {
    name: 'HomeView',
    components:{
      FtContainer,
      ConfigModal,
      RowDataModal,
      'easy-data-table': Vue3EasyDataTable,
    },
    data(){
      return {
        res: {},
        tableSpec: JSON.parse(JSON.stringify(defaultTableSpec)),
        error: false,
        success: false,
        showModal: {
          'rowData': false,
          'config': false
        },
        loadValue: null,
        loadOptions: [],
        selectedRow: {},
        selectedRowData: {},
        
      }
    },
    created(){
      this.loadTable();
      this.getSettings();
    },
    methods:{
      loadTable(){
        this.axios.get('/home', {params: {'spec': JSON.stringify(this.tableSpec)}}).then(data => {
          this.success = true;
          this.res = data.data;
        }).catch(error => {
          this.error = true;
          this.res = error;
        });
      },
      getSettings(){
          this.axios.get(`/get-settings`).then(data => {
              this.loadOptions = data.data.settings;
          }).catch(error => {
              alert('Failed To Get Settings');
          })
      },
      loadSetting(){
          if(!this.loadValue){
            this.tableSpec = JSON.parse(JSON.stringify(defaultTableSpec));
            this.loadTable();
            return;
          }
          this.axios.get(`/load-setting/${this.loadValue.value}`).then(data => {
              this.tableSpec = data.data.setting;
              this.loadTable();
          }).catch(error => {
              alert('Failed To Get Settings');
              console.log(error);
          })
      },
      showRow(row){
        this.selectedRow = row;
        this.axios.get(`/home-spec`, {params: {'spec': JSON.stringify(row)}}).then(data => {
          this.selectedRow = row;
          this.showModal.rowData = true;
          data.data.row = {
            ...data.data.row,
            ...row
          }
          this.selectedRowData = data.data;
        }).catch(error => {
          this.res = error;
        });
      },
      downloadData(){
        if(this.res.rows){
          downloadCSV(this.res.rows);
        }
      }
    }
  };
</script>

<style lang="scss">
  @import 'vue3-easy-data-table/dist/style.css';

  .home-div {
    color: $primary;
  }
  .customize-table * {
    font-family: 'Times New Roman', Times, serif !important;
  }

  .customize-table {
    --easy-table-border: 1px solid #bcd4e6;
    --easy-table-row-border: 1px solid rgba(0, 0, 0, 0.12);

    --easy-table-header-font-size: 16px;
    --easy-table-header-height: 50px;
    --easy-table-header-font-color: rgb(41, 50, 65);
    --easy-table-header-background-color: rgb(214, 226, 233);

    --easy-table-header-item-padding: 10px 15px;

    --easy-table-body-even-row-font-color: rgb(41, 50, 65);
    --easy-table-body-even-row-background-color: rgba(214, 226, 233, 0.2);

    --easy-table-body-row-font-color: rgb(41, 50, 65);
    --easy-table-body-row-background-color: #fff;
    --easy-table-body-row-height: 50px;
    --easy-table-body-row-font-size: 16px;

    --easy-table-body-row-hover-font-color: rgba(0, 0, 0, 0.7);
    --easy-table-body-row-hover-background-color: rgba(230, 238, 240, 0.9);
    --easy-table-body-row-hover-cursor: pointer;

    --easy-table-body-item-padding: 10px 15px;

    --easy-table-footer-background-color: #fff;
    --easy-table-footer-font-color: rgba(0, 0, 0, 0.7);
    --easy-table-footer-font-size: 16px;
    --easy-table-footer-padding: 0px 10px;
    --easy-table-footer-height: 50px;

    --easy-table-rows-per-page-selector-width: 70px;
    --easy-table-rows-per-page-selector-option-padding: 10px;
    --easy-table-rows-per-page-selector-z-index: 1;


    --easy-table-scrollbar-track-color: #2d3a4f;
    --easy-table-scrollbar-color: #2d3a4f;
    --easy-table-scrollbar-thumb-color: #4c5d7a;;
    --easy-table-scrollbar-corner-color: #2d3a4f;

    --easy-table-loading-mask-background-color: #fff;
  }
  .customize-table > div > table > tbody {
    cursor: pointer;
  }
</style>