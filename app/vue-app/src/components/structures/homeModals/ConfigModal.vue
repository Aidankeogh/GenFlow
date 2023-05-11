<template>
    <ft-modal @close="$emit('close')" width="90%">
        <template #header>
            Data Settings
        </template>
        <div class="ft-p-2">
            <ft-ace 
                @init="initEditor"
                v-model:value="tableSpec"
                class="ft-ace-editor"
                lang="json"
                height="300px"
                width="100%">
            </ft-ace>
            <div class="ft-d-flex ft-justify-content-center ft-mt-3">
                <button @click="parseSpec" :disabled="validSpec" class="ft-btn ft-border ft-btn-light ft-hover-text-white ft-hover-bg-ft ft-w-50"> Apply</button>
            </div>
        </div>
    </ft-modal>

</template>

  
<script>
    import FtModal from '@/components/utils/ft-modal/FtModal.vue';
    import FtAce from '../../utils/ft-ace/FtAce.vue';

    export default {
        name: 'config-modal',
        components:{
            FtModal,
            FtAce
        },
        props:{
            intialTableSpec: {required:true}
        },
        data(){
            return {
                tableSpec: JSON.stringify(this.intialTableSpec, null, '\t')
            }
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
                    this.$emit('update:intialTableSpec', JSON.parse(this.tableSpec));
                    this.$emit('close');
                } catch(err){
                    alert('Invalid JSON')
                    this.validSpec = false;
                }
            },
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