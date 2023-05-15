<template>
    <ft-container>
      <template #title>
        <span class="ft-d-flex">
          <label> Create Dashboard</label>
          <label @click="showModal.config=true" class="ft-hover-text ft-pl-2"><font-awesome-icon :icon="['fas', 'gear']" /></label>
          <label @click="addComp" class="ft-hover-text ft-pl-2"><font-awesome-icon :icon="['fas', 'circle-plus']" /></label>
        </span>
      </template>
      <!-- <div v-if="!res.success" class="resp-div"> Server Response: {{JSON.stringify(res)}}</div> -->
      <div class="ft-chart" v-if="res.success">
        
      </div>
      <div>
        <ft-grid-layout ref="ftGrid"></ft-grid-layout>
      </div>
    </ft-container>
  </template>

  <script>
    import FtContainer from '@/components/utils/ft-container/FtContainer.vue';
    import FtGridLayout from '../components/structures/ft-grid-layout/FtGridLayout.vue'; 

    export default {
      name: 'create-view',
      components: {
        FtContainer,
        FtGridLayout
      },
      data(){
        return {
          res: {},
          custom: {},
          showModal: {
            config: false,
            addComponent: false
          }
        }
      },
      methods:{
        addComp(){
          this.$refs.ftGrid.addComp();
        }
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