<template>
  <ft-container>
    <template #title>
      <span class="ft-d-flex">
        <label> Create Dashboard</label>
        <label @click="showModal.config=true" class="ft-hover-text ft-pl-2"><font-awesome-icon :icon="['fas', 'gear']" /></label>
        <label @click="addComp" class="ft-hover-text ft-pl-2"><font-awesome-icon :icon="['fas', 'circle-plus']" /></label>
        <label @click="toggleFullscreen" class="ft-hover-text ft-pl-2"><font-awesome-icon :icon="['fas', 'expand']" /></label>
      </span>
    </template>
    <!-- <div v-if="!res.success" class="resp-div"> Server Response: {{JSON.stringify(res)}}</div> -->
    <div>
      <ft-grid-layout v-model:modelValue="dashboardInitialValue" mode="create" ref="ftGrid"></ft-grid-layout>
      <dash-config-modal v-model:intialDashSpec="dashboardInitialValue" v-if="showModal.config" @close="showModal.config=false"></dash-config-modal>
      <div ref="fullscreenElement">
        <div v-if="isFullScreen">
          <ft-grid-layout ref="gridLayout" v-model:modelValue="dashboardInitialValue" mode="view"></ft-grid-layout>
        </div>
      </div>
    </div>
  </ft-container>
</template>

<script>
  import FtContainer from '@/components/utils/ft-container/FtContainer.vue';
  import FtGridLayout from '@/components/structures/ft-grid-layout/FtGridLayout.vue'; 
  import DashConfigModal from '@/components/structures/create-modals/DashConfigModal.vue';

  export default {
    name: 'create-view',
    components: {
      FtContainer,
      FtGridLayout,
      DashConfigModal
    },
    data(){
      return {
        isFullScreen: false,
        dashboardInitialValue: {
          colNum: 24,
          rowHeight: 10,
          layout: [
                  { x: 0, y: 0, w: 6, h: 10, i: 0, comp: {component: 'ft-markdown', bind: {'markdown': '### Aloha !'}}  }
              ]
        },
        showModal: {
          config: false
        }
      }
    },
    mounted() {
      document.addEventListener("fullscreenchange", this.handleFullscreenChange);
    },
    beforeDestroy() {
      document.removeEventListener("fullscreenchange", this.handleFullscreenChange);
    },
    methods:{
      addComp(){
        this.$refs.ftGrid.addComp();
      },
      toggleFullscreen() {
        const element = this.$refs.fullscreenElement;
        element.requestFullscreen().then(() => {
          this.$nextTick(() => 
            setTimeout(() => this.$refs.gridLayout.resizeAll(), 200) 
          );
        }).catch(err => {
          console.error(`Error attempting to enable fullscreen: ${err.message}`);
        });
      },
      handleFullscreenChange() {
        this.isFullScreen = !this.isFullScreen;
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