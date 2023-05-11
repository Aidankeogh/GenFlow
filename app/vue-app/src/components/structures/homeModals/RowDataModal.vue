<template>
    <ft-modal @close="$emit('close')" width="90%">
        <template #header>
            Selected Row
        </template>
        <div class="">
            <pre>{{ JSON.stringify(selectedRowData, null, 4)}}</pre>
        </div>
    </ft-modal>

</template>

  
<script>
    import FtModal from '@/components/utils/ft-modal/FtModal.vue';

    export default {
        name: 'row-data-modal',
        components:{
            FtModal
        },
        props:{
            selectedRow: {requried:true},
            selectedRowData: {requried:true},
        }
    }

</script>