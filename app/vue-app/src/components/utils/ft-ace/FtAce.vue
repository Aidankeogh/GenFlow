<template>
    <div ref="my_editor" :style="c_style"></div>
  </template>
  
  <script>
    import Ace from 'ace-builds'
    import 'ace-builds/src-noconflict/theme-chrome'
    import 'ace-builds/src-noconflict/mode-text'

    Ace.config.set('basePath', '/node_modules/ace-builds/src-noconflict');


    export default {
      name: 'ft-ace',
      props: {
        value: { type: String, required: true },
        lang: { type: String, default: 'text' },
        theme: { type: String, default: 'chrome' },
        options: { type: Object },
        placeholder: { type: String },
        height: { default: '300px'},
        width: { default: ''},
        fontSize: { default: "16px"}
      },
      data(){
        return {
          editor: null,
          contentBackup: ''
        }
      },
      mounted() {
        let vm = this;
        let lang = this.lang||'text';
        let theme = this.theme||'chrome';
  
        let editor = vm.editor = Ace.edit(this.$refs.my_editor);
        editor.$blockScrolling = Infinity;
  
        this.$emit('init',editor);
  
        //editor.setOption("enableEmmet", true);
        editor.getSession().setMode('ace/mode/' + lang );
        editor.setTheme('ace/theme/'+theme);
        editor.setFontSize(this.fontSize)
  
        if(this.value){
          editor.setValue(this.value, 1);
        }
        this.contentBackup = this.value;
  
        editor.on('change',function () {
          console.log('mahalo')
          let content = editor.getValue();
          vm.$emit('update:value', content);
          vm.contentBackup = content;
        });
        if(vm.options) editor.setOptions(vm.options);
      },
      methods: {
        focus() {
          this.editor.focus();
        },
        blur() {
          this.editor.blur();
        },
        selectAll() {
          this.editor.selectAll();
        }
      },
      beforeUnmount() {
          let _a, _b;
          (_b = this.editor) === null || _b === void 0 ? void 0 : _b.destroy();
      },
      watch: {
        value(val) {
          if (this.contentBackup !== val) {
            this.editor.setValue(val, 1);
            this.contentBackup = val;
          }
        },
        theme(val) {
          this.editor.setTheme('ace/theme/' + val);
        },
        options(val) {
          this.editor.setOptions(val);
        },
        placeholder(val) {
          this.editor.setOption('placeholder', val);
        },
        lang(val) {
          this.editor.setOption('mode', 'ace/mode/' + val);
        },
        height:function(){
          this.$nextTick(function(){
            this.editor.resize()
          })
        },
        width:function(){
          this.$nextTick(function(){
            this.editor.resize()
          })
        }
      },
      computed: {
        c_style: function() {
          let height = this.height ? this.height : '100%'
          let width = this.width ? this.width : '100%'
          return `height:${height}; width:${width};`;
        }
      }
    }
  </script>