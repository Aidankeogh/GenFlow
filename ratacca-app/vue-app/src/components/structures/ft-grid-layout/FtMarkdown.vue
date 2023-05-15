<template>
    <div v-html="compiledMarkdown"></div>
</template>

<script>
    import * as marked from 'marked';

    export default {
        name: 'ft-markdown',
        props: {
            markdown:{default: '### This is a Markdown'}
        },
        computed: {
            compiledMarkdown(){
                return marked.marked(this.markdown);
            }
        }
    }


</script>