<template>
    <ft-modal @close="$emit('close')" width="90%">
        <template #header>
            {{ modeTitle }}
        </template>
        <div class="ft-p-2">
            <div class="ft-d-flex ft-mb-3">
                <span class="ft-d-flex ft-flex-column ft-w-50">
                    <label class="ft-mb-1" style="font-weight: bold;"> Component </label>
                    <v-select 
                        class="ft-w-50"
                        v-model:modelValue="selVal"
                        :options="compOptions"
                        :clearable="false"
                    ></v-select>
                </span>
            </div>
            <div v-if="selVal.value=='ft-markdown'">
                <ft-ace 
                    @init="initEditor"
                    v-model:value="markdownCode"
                    class="ft-ace-editor"
                    lang="markdown"
                    height="450px"
                    width="100%">
                </ft-ace>
            </div>
            <div v-if="selVal.value=='ft-echartsJs'">
                <span class="ft-d-flex ft-flex-column ft-w-50 ft-mb-3">
                    <label class="ft-mb-1" style="font-weight: bold;"> Fetch Data Settings</label>
                    <v-select 
                        class="ft-w-50"
                        ref="vSelectMultiple"
                        v-model:modelValue="dataValues"
                        :options="loadOptions"
                        :clearable="true"
                        :multiple="true"
                    ></v-select>
                </span>
                <ft-ace 
                    @init="initEditor"
                    v-model:value="jsCode"
                    class="ft-ace-editor"
                    lang="javascript"
                    height="450px"
                    width="100%">
                </ft-ace>
            </div>
            <div v-if="selVal.value=='ft-select'">
                <ft-ace 
                    @init="initEditor"
                    v-model:value="selectJson"
                    class="ft-ace-editor"
                    lang="json"
                    height="450px"
                    width="100%">
                </ft-ace>
            </div>
            <div class="ft-d-flex ft-justify-content-center ft-mt-3">
                <button @click="confirmChanges" class="ft-btn ft-border ft-btn-light ft-hover-text-white ft-hover-bg-ft ft-w-50">
                    {{ modeTitle }}
                </button>
            </div>
        </div>
    </ft-modal>
</template>

<script>
    import FtModal from '@/components/utils/ft-modal/FtModal.vue';
    import FtAce from '@/components/utils/ft-ace/FtAce.vue';
    import _ from 'lodash';

    const compRef = {
        'ft-markdown': 'Markdown',
        'ft-echartsJs': 'Echarts Js',
        'ft-select': 'Select Option'
    }

    const defaultJs = `option = {
  title: {
    text: 'Aloha Echarts',
    left: 'center'
  },
  xAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [150, 230, 224, 218, 135, 147, 260],
      type: 'line'
    }
  ]
};
return option;
`
    const defaultSelectProps = JSON.stringify({initialValue: null, label: "", bind: {}}, null, 4);

    export default {
        name: 'item-modal',
        components:{
            FtModal,
            FtAce
        },
        props:{
            mode:{default: 'create'},
            initialItem: {default: () => {return {}}}
        },
        computed:{
            modeTitle(){
                const titleRef = {
                    'create': 'Add Component',
                    'edit': 'Update Component'
                }
                return titleRef[this.mode]
            }
        },
        mounted(){
            this.getSettings()
        },
        data(){
            return {
                loadOptions: [],
                dataValues: _.get(this.initialItem, 'comp.bind.dataValues', []),
                selVal: {
                    'value': _.get(this.initialItem, 'comp.component', 'ft-markdown'),
                    'label' : compRef[_.get(this.initialItem, 'comp.component', 'ft-markdown')],
                }, 
                markdownCode: _.get(this.initialItem, 'comp.bind.markdown', '### This is a Markdown'),
                selectJson: _.get(this.initialItem, 'comp.bind.propsJson', defaultSelectProps),
                jsCode: _.get(this.initialItem, 'comp.bind.js', defaultJs),
                compOptions: Object.keys(compRef).map(key => {
                    return {value: key, label: compRef[key]}
                })
            }
        },
        methods:{
            initEditor(editor){
                editor.renderer.setScrollMargin(3, 0);
                editor.setOptions({
                    printMargin: true,
                    wrap: true,
                    scrollPastEnd: 0.5,
                });
            },
            confirmChanges(){
                this.$emit(this.mode + 'Item', {
                    ...this.initialItem, 
                    comp: {
                        ...this.getComp()
                    }
                })
            },
            getComp(){
                switch (this.selVal.value){
                    case 'ft-markdown':
                        return {
                            component: this.selVal.value,
                            bind: {markdown: this.markdownCode}
                        }
                    case 'ft-echartsJs':
                        return {
                            component: this.selVal.value,
                            bind: {
                                js: this.jsCode,
                                dataValues: this.dataValues
                            }
                        }
                    case 'ft-select':
                        try{
                            JSON.parse(this.selectJson)
                        }catch(err){
                            alert('Invalid Json')
                            return;
                        }
                        return {
                            component: this.selVal.value,
                            bind: {
                                propsJson: this.selectJson
                            }
                        }
                    default:
                        return null;
                }
            },
            getSettings(){
                this.axios.get(`/get-settings`).then(data => {
                    this.loadOptions = data.data.settings;
                }).catch(error => {
                    alert('Failed To Get Settings');
                })
            },
        }
    }
</script>