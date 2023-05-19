<template>
    <div>
        <grid-layout
            v-model:layout="layout"
            :col-num="modelValue.colNum"
            :row-height="modelValue.rowHeight"
            :vertical-compact="false"
            :is-draggable="mode=='create'"
            :is-resizable="mode=='create'"
        >
            <template #default="{ gridItemProps }">
                <grid-item 
                    @resized="resize"
                    v-for="item in layout" :key="item.i"  
                    v-bind="gridItemProps"
                    :x="item.x"
                    :y="item.y"
                    :w="item.w"
                    :h="item.h"
                    :i="item.i"
                    >
                    <ft-grid-item 
                        :ref="'gridItem' + item.i"
                        @delete="deleteComp(item.i)"
                        @edit="editComp(item.i)"
                        :comp="item.comp"
                        :mode="mode"
                        :itemId="'item' + item.i"
                    >
                    </ft-grid-item>
                </grid-item>
            </template>
        </grid-layout>
        <item-modal 
            v-if="showModal.component" 
            @close="showModal.component=false"
            @createItem="addItem"
            @editItem="editItem"
            :mode="itemModalMode"
            :initialItem="initialItem"
        >
        </item-modal>
    </div>
</template>

<script>
    import FtGridItem from './FtGridItem.vue';
    import itemModal from '../create-modals/itemModal.vue';

    export default {
        name: 'ft-grid-layout',
        components:{
            FtGridItem,
            itemModal
        },
        props:{
            modelValue:{
                required: true
            },
            mode:{default: 'create'}
        },
        computed:{
            maxY(){
                let maxY = 0;
                this.layout.forEach(item => {
                    if(item.y > maxY){ maxY = item.y }
                })
                return maxY + 1;
            }
        },
        mounted(){
            this.resizeAll();
        },
        data () {
            return {
                itemModalMode: 'create',
                initialItem: {},
                layout: this.modelValue.layout,
                showModal:{
                    component: false
                }
            }
        },
        watch:{
            modelValue: {
                handler(newValue, oldValue) {
                    this.layout = this.modelValue.layout;
                },
                deep: true
            }
        },
        methods:{
            resize(index){
                let itemName = 'gridItem' + index;
                this.$refs[itemName][0].resize();
            },
            resizeAll(){
                this.$nextTick(() => {
                    this.layout.forEach(item => this.resize(item.i));
                })
            },
            addComp(){
                this.initialItem = {
                    x: 0,
                    y: this.maxY,
                    w: 6,
                    h:10,
                    i: this.layout.length,
                    comp: {}
                }
                this.itemModalMode = 'create';
                this.showModal.component = true;
            },
            addItem(item){
                this.layout.push(item);
                this.$emit('update:modelValue', {
                    ...this.modelValue,
                    layout: this.layout
                })
            },
            editComp(itemI){
                this.initialItem = this.layout[itemI]
                this.itemModalMode = 'edit';
                this.showModal.component = true;
            },
            editItem(item){
                this.layout[item.i] = item;
                this.$emit('update:modelValue', {
                    ...this.modelValue,
                    layout: this.layout
                })
            },
            deleteComp(itemI){
                let newLayout = [];
                let i = 0;
                let removed = false;
                this.layout.forEach((item) => {
                    if(i == itemI && !removed){
                        removed = true;
                        return;
                    }
                    newLayout.push({...item, i: i});
                    i ++;
                });
                this.layout = newLayout;
                this.$emit('update:modelValue', {
                    ...this.modelValue,
                    layout: this.layout
                })
            }
        }
    }
</script>

<style>
    .vue-grid-item {
        background-color: transparent !important;
    }
</style>