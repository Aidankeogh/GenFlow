<template>
    <ft-container>
      <template #title><label> Experiments Table</label></template>
      <!-- <div class="home-div ft-pt-2 ft-pl-2"> Server Response: {{JSON.stringify(res)}}</div> -->
        <div v-if="res.rows">
          <easy-data-table
            :headers="res.columns"
            :items="res.rows"
            buttons-pagination
            table-class-name="customize-table"
            header-text-direction="center"
            body-text-direction="center"
          />
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


    export default {
      name: 'HomeView',
      components:{
        FtContainer,
        'easy-data-table': Vue3EasyDataTable,
      },
      data(){
        return {
          res: {},
          error: false,
          success: false
        }
      },
      created(){
        this.axios.get('/home').then(data => {
          this.success = true;
          this.res = data.data;
        }).catch(error => {
          this.error = true;
          this.res = error;
        });
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
      
      --easy-table-border: 1px solid rgba(0, 0, 0, 0.12);
      --easy-table-row-border: 1px solid rgba(0, 0, 0, 0.12);

      --easy-table-header-font-size: 16px;
      --easy-table-header-height: 50px;
      --easy-table-header-font-color: rgba(0, 0, 0, 0.9);
      --easy-table-header-background-color: #fff;

      --easy-table-header-item-padding: 10px 15px;

      --easy-table-body-even-row-font-color: rgba(0, 0, 0, 0.7);
      --easy-table-body-even-row-background-color: #fff;

      --easy-table-body-row-font-color: rgba(0, 0, 0, 0.7);
      --easy-table-body-row-background-color: #fff;
      --easy-table-body-row-height: 50px;
      --easy-table-body-row-font-size: 16px;

      --easy-table-body-row-hover-font-color: rgba(0, 0, 0, 0.7);
      --easy-table-body-row-hover-background-color: #fff;

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
  </style>