<template>
    <div
      class="ft-input-wrapper ft-d-flex ft-align-items-center ft-bg-white"
      :class="{'focus': active}">
      <input
        v-on="listeners"
        v-bind="$attrs" 
        @keyup.enter="$emit('enter')"
        @focus="focus"
        @blur="blur"
        v-model="val"
        class="ft-w-100"
        :placeholder="placeholder"
        :readonly="readonly"
        style="outline: none !important;"
    />
    </div>
  </template>
  
  <script>  
    export default {
      name: 'ft-input',
      props:{
        modelValue: {default: ''},
        placeholder:{default: ''},
        type: {default: ''},
        readonly:{default: false},
        i_mask:{default: ()=> {return {}}}
      },
      data() {
        return {
          val: this.modelValue,
          active: false,
        }
      },
      computed:{
        listeners(){
          return {
            ...this.$listeners,
            'input': event => this.$emit('input', event.target.value)
          }
        }
      },
      methods:{
        focus(){
          this.active = true;
        },
        blur(){
          this.active = false;
        },
      },
      watch:{
        modelValue(value){
          this.val = value;
        }
      }
    }
  </script>
  
  <style lang="scss">
     .ft-input-wrapper{
      cursor:pointer;
      position:relative;
      height:34px;
      border: 1px solid rgba(60, 60, 60, 0.26);
      border-radius: 4px;
    }
  
    .ft-input-wrapper.error_input {
      color:rgb(242, 19, 93);
      border-color: rgb(242, 19, 93);
    }
    .ft-input-wrapper.error_input * {
      color:rgb(242, 19, 93);
    }
  
    .ft-input-wrapper *{
      cursor:pointer;
    }
  
    .ft-input-wrapper input {
      border: none;
      color:rgb(20, 67, 82);
    }
  
    .ft-input-wrapper.focus{
      border: 1px solid #2486be;
    }
  
    .ft-input-wrapper.focus *{
      color: #2486be;
    }
    .ft-input-wrapper.focus  input::placeholder{
      color: #2486be;
    }
  
  </style>