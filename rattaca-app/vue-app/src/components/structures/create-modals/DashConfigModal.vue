<template>
    <ft-modal @close="$emit('close')" width="90%">
        <template #header>
            Dashboard Settings
        </template>
        <div class="ft-p-2">
            <div class="ft-d-flex ft-flex-wrap ft-mb-3">
                <span style="min-width: 340px" class="ft-d-flex ft-flex-column ft-w-50 ft-mt-2">
                    <label class="ft-mb-1" style="font-weight: bold;">Load Setting</label>
                    <span class="ft-d-flex">
                        <v-select 
                            class="ft-w-50"
                            v-model:modelValue="loadValue"
                            :options="loadOptions">
                            <template #no-options="{ search, searching, loading }">
                                No Dashboard Setting Created
                            </template>
                        </v-select>
                        <button @click="loadSetting" class="ft-btn ft-border ft-btn-light ft-hover-text-white ft-hover-bg-ft "> Load</button>
                        <button @click="deleteSetting" class="ft-btn ft-border ft-btn-light ft-hover-text-white ft-hover-bg-danger "><font-awesome-icon :icon="['fas', 'trash-can']" /></button>
                    </span>
                </span>
                <span style="min-width: 340px" class="ft-d-flex ft-flex-column ft-w-50 ft-mt-2">
                    <label class="ft-mb-1" style="font-weight: bold;">Save Setting As</label>
                    <span class="ft-d-flex">
                        <ft-input v-model:modelValue="saveAs"  class="ft-w-50"></ft-input>
                        <button @click="saveSettings" class="ft-btn ft-border ft-btn-light ft-hover-text-white ft-hover-bg-ft "> Save</button>
                    </span>
                </span>
            </div>
            <label class="ft-mb-1" style="font-weight: bold;"> Dashboard Spec </label>
            <ft-ace 
                @init="initEditor"
                v-model:value="dashSpec"
                class="ft-ace-editor"
                lang="json"
                height="410px"
                width="100%">
            </ft-ace>
            <div class="ft-d-flex ft-justify-content-center ft-mt-3">
                <button @click="parseSpec" class="ft-btn ft-border ft-btn-light ft-hover-text-white ft-hover-bg-ft ft-w-50"> Apply</button>
            </div>
        </div>
    </ft-modal>

</template>

  
<script>
    import FtModal from '@/components/utils/ft-modal/FtModal.vue';
    import FtAce from '../../utils/ft-ace/FtAce.vue';
    import FtInput from '../../utils/ft-input/FtInput.vue';
    
    export default {
        name: 'dash-config-modal',
        components:{
            FtModal,
            FtAce,
            FtInput
        },
        props:{
            intialDashSpec: {required:true}
        },
        data(){
            return {
                dashSpec: JSON.stringify(this.intialDashSpec, null, '\t'),
                loadOptions: [],
                loadValue: null,
                saveAs: ''
            }
        },
        created(){
            this.getSettings()
        },
        mounted(){
            this.dashSpec = JSON.stringify(this.intialDashSpec, null, '\t');
        },
        methods: {
            initEditor(editor){
                editor.renderer.setScrollMargin(3, 0);
                editor.setOptions({
                    printMargin: true,
                    wrap: true,
                    scrollPastEnd: 0.5,
                });
            },
            parseSpec(){
                try{
                    this.$emit('update:intialDashSpec', JSON.parse(this.dashSpec));
                    this.$emit('close');
                } catch(err){
                    alert('Invalid JSON');
                }
            },
            getSettings(){
                this.axios.get(`/get-dashs`).then(data => {
                    this.loadOptions = data.data.settings;
                }).catch(error => {
                    alert('Failed To Get Settings');
                    console.log(error);
                })
            },
            saveSettings(){
                if(!this.saveAs){
                    alert('Invalid Name');
                    return;
                }
                this.axios.post(`/save-dash`, {
                    setting_name: this.saveAs,
                    setting_data: JSON.parse(this.dashSpec)
                }).then(data => {
                    this.getSettings()
                    alert('Setting Saved Successfully');
                }).catch(error => {
                    alert('Invalid Setting');
                    console.log(error);
                })
            },
            loadSetting(){
                if(!this.loadValue){
                    this.dashSpec = JSON.stringify(this.intialDashSpec, null, '\t');
                    return;
                }
                this.axios.get(`/load-dash/${this.loadValue.value}`).then(data => {
                    this.dashSpec = JSON.stringify(data.data.setting, null, '\t');
                }).catch(error => {
                    alert('Failed To Get Settings');
                    console.log(error);
                })
            },
            deleteSetting(){
                if(!confirm('Do you really want to delete this setting ?')){
                    return;
                }
                this.axios.post(`/delete-dash`, {
                    setting_name: this.loadValue.value
                }).then(data => {
                    this.getSettings()
                    alert('Setting Deleted Successfully');
                }).catch(error => {
                    alert('Invalid Setting');
                    console.log(error);
                })

            }
        }
    }

</script>

<style>
    .ft-ace-editor {
        border: 1px solid lighgray;
        border-radius: 5px;
        box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.1);
    }
</style>