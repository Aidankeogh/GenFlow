<template>
    <div class="ft-grid-item ft-w-100 ft-p-1" style="height:100%; min-width:100%">
        <div v-if="mode=='create'" class="ft-d-flex ft-justify-content-end ft-align-items-center">
            <div class="ft-d-flex ft-flex-wrap ft-mr-2 ft-mt-2">
                <label @click="$emit('edit')" class="ft-hover-text ft-pl-2">
                    <font-awesome-icon :icon="['fas', 'pen-to-square']" />
                </label>
                <label @click="$emit('delete')" class="ft-hover-text ft-pl-2">
                    <font-awesome-icon :icon="['fas', 'trash-can']" />
                </label>
            </div>
        </div>
        <component :is="comp.component" v-bind="comp.bind">
            
        </component>
    </div>
</template>

<script>
    import FtMarkdown from './FtMarkdown.vue';
    export default {
        name: 'ft-grid-item',
        components:{
            FtMarkdown
        },
        props:{
            comp:{required:true},
            mode:{default: 'create'}
        }
    }
</script>

<style>
    .ft-grid-item{
        background-color: #fff;
        border: none !important;
        border-radius: 15px !important;
        box-shadow: 0px 0px 25px lightgray !important;
    }
</style>