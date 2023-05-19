<template>
    <ft-container>
      <template #title>
        <span class="ft-d-flex">
          <label> Dashboards Page</label>
        </span>
        <span class="ft-d-flex ft-pt-2" style="width:250px;">
          <v-select
            class="ft-w-100" 
              v-if="loadOptions"
              v-model:modelValue="loadValue"
              :options="loadOptions">
              <template #no-options="{ search, searching, loading }">
                  No Dashboards Created
              </template>
          </v-select>
          <button @click="loadSetting" class="ft-btn ft-border ft-btn-light ft-hover-text-white ft-hover-bg-ft "> Load</button>
        </span>
      </template>
      <div v-if="Object.keys(dashboardModel).length" style="min-height:90vh;">
        <ft-grid-layout ref="gridLayout" :modelValue="dashboardModel" mode="view"></ft-grid-layout>
      </div>
    </ft-container>
  </template>

  <script>
    import FtContainer from '@/components/utils/ft-container/FtContainer.vue';
    import FtGridLayout from '@/components/structures/ft-grid-layout/FtGridLayout.vue'; 

    export default {
      name: 'dashboards-view',
      components: {
        FtContainer,
        FtGridLayout
      },
      data(){
        return {
          loadValue: null,
          loadOptions: [],
          dashboardModel: {}
        }
      },
      mounted(){
        this.getSettings()
      },
      methods:{
        getSettings(){
          this.axios.get(`/get-dashs`).then(data => {
              this.loadOptions = data.data.settings;
          }).catch(error => {
              alert('Failed To Get Settings');
              console.log(error);
          })
        },
        loadSetting(){
          if(!this.loadValue){
              this.dashboardModel = {}
              return;
          }
          this.axios.get(`/load-dash/${this.loadValue.value}`).then(data => {
            this.dashboardModel = data.data.setting;
            this.$nextTick(() => 
                setTimeout(() => this.$refs.gridLayout.resizeAll(), 200) 
              );
          }).catch(error => {
              alert('Failed To Get Settings');
              console.log(error);
          })
        },
      }
    };
  </script>

  <style lang="scss">
    .resp-div {
      color: $primary;
    }
    .ft-chart {
      width: 100%;
    }

    .ft-chart span {
      display: block;
      padding-top: 0.5rem;
    }

  </style>