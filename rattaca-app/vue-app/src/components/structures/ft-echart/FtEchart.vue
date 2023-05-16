<template>
    <div 
      ref="my_echart" 
      class="ft-echart-wrapper"
      >
    </div>
</template>

<script>
  import * as echarts from 'echarts';

  import { FtTheme } from './theme';
  import _ from 'lodash';
  var myChart = {};

  export default {
    name: 'ft-echart',
    props: {
      echartOption: {required:true}
    },
    created(){
      echarts.registerTheme('ft-theme', FtTheme);
    },
    mounted(){
        this.initialize()
    },  
    methods: {
      initialize(){
        myChart = echarts.init(this.$refs.my_echart, 'ft-theme');        
        myChart.setOption(this.echartOption);
        this.$emit('init', myChart);
      }
    }
  }

</script>

<style>
  .ft-echart-wrapper {
    width: 100%;
    height: 100%;
    
  }
</style>