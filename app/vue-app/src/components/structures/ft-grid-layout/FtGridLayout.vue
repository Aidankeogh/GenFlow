<template>
    <div>
        <grid-layout
            v-model:layout="layout"
            :col-num="24"
            :row-height="10"
            :vertical-compact="false"
        >
            <template #default="{ gridItemProps }">
                <grid-item 
                    v-for="item in layout" :key="item.i"  
                    v-bind="gridItemProps"
                    :x="item.x"
                    :y="item.y"
                    :w="item.w"
                    :h="item.h"
                    :i="item.i"
                    >
                    <ft-grid-item @delete="deleteComp(item.i)" @edit="editComp(item.i)" :comp="item.comp">
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
        name: 'ft-frid-layout',
        components:{
            FtGridItem,
            itemModal
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
        data () {
            return {
                itemModalMode: 'create',
                initialItem: {},
                layout: [
                    { x: 0, y: 0, w: 6, h: 10, i: 0, comp: {component: 'ft-markdown', bind: {'markdown': '### Aloha !'}}  }
                ],
                showModal:{
                    component: false
                }
            }
        },
        methods:{
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
            },
            editComp(itemI){
                this.initialItem = this.layout[itemI]
                this.itemModalMode = 'edit';
                this.showModal.component = true;
            },
            editItem(item){
                this.layout[item.i] = item;
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
            }
        }
    }
</script>