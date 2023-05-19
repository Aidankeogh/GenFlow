<template>
    <div style="height: 100%;">
        <ft-echart 
            v-if="Object.keys(echartOption).length"
            ref="echart"
            :key="echartKey" 
            :echartOption="echartOption"
            :itemId="itemId"
            >
        </ft-echart>
    </div>
</template>

<script>
    import FtEchart from '@/components/structures/ft-echart/FtEchart.vue';
    import { runJsCode } from './utils';
    
    export default {
        name: 'ft-echart-js',
        components: {
            FtEchart
        },
        props: {
            itemId: {required: true},
            js:{required: true},
            dataValues: {default: ()=> {return []}},
        },
        data(){
            return {
                echartOption: {},
                echartKey: 0,
                tableDfs: {}
            }
        },
        mounted(){
           this.getOption();
        },
        methods:{
            getOption(){
                let promises = this.dataValues.map(data => {
                    return this.loadSetting(data.value);
                })
                Promise.all(promises).then(()=> {
                    try {
                        let args = {'tables': JSON.parse(JSON.stringify(this.tableDfs))};
                        console.log(`==== Args ====`, {args});
                        this.echartOption = runJsCode(this.js, args);
                        console.log(`==== echartOption ====`, JSON.parse(JSON.stringify(this.echartOption)));
                        this.echartKey ++;
                    }catch(error){
                        console.error('ECharts JS Code Error', error);
                    }
                }).catch((error) =>{
                    console.error('Promises error', error);
                });
            },
            resize(){
                this.$refs.echart.resize()
            },
            loadSetting(dataValue){
                return new Promise((resolve, reject) => {
                    this.axios.get(`/load-setting/${dataValue}`).then(data => {
                        this.axios.get('/home', {params: {'spec': JSON.stringify(data.data.setting)}}).then(data => {
                            this.tableDfs[dataValue] = data.data.rows;
                            resolve();
                        }).catch(error => {
                            alert(`Failed To Fetch Df ${dataValue}`);
                            console.error(`${dataValue}`, error);
                        });
                    }).catch(error => {
                        alert(`Failed To Get Settings ${dataValue}`);
                        console.error(`${dataValue}`, error);
                        reject();
                    })
                });   
            }
        },
        watch:{
            js(){
                this.getOption();
            }
        }
    }


</script>