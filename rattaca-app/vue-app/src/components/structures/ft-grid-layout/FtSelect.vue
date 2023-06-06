<template>
    <div class="ft-d-flex ft-flex-column">
        <label> {{ specs.label }} </label>
        <v-select
            @update:modelValue="updateSelect"
            v-model:modelValue="selectValue"
            v-bind="specs.bind">
        </v-select>
    </div>
    
</template>

<script>
    import _ from 'lodash';

    export default {
        name: 'ft-select',
        props:{
            itemId: {required: true},
            propsJson: {required: true},
            globals: {default: ()=>{return {}}}
        },
        data(){
            return {
                specs: JSON.parse(this.propsJson),
                selectValue: _.get(this.globals, `${this.itemId}`, JSON.parse(this.propsJson).initialValue)
            }
        },
        mounted(){
            if(this.selectValue){
                this.updateSelect(this.selectValue)
            }
        },
        methods:{
            updateSelect(value){
                this.$emit('updateGlobals', {
                    itemId: this.itemId,
                    value: value
                })
            }
        },
        watch:{
            propsJson(){
                this.specs = JSON.parse(this.propsJson);
                this.selectValue = _.get(this.globals, `${this.itemId}`, JSON.parse(this.propsJson).initialValue);
                this.updateSelect(this.selectValue);
            }
        }
    }
</script>