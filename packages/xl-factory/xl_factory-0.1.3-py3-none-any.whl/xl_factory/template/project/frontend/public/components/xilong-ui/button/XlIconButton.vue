<script setup>
const emits = defineEmits('click')

const props = defineProps({
    type: {},
    code: {},
    disabled: {},
    loading: {},
    icon: {},
    l: {}
});
</script>

<template>
    <xl-button v-bind="$props" @click="() => emits('click')">
        <i class="iconfont">{{ code }}</i>
    </xl-button>
</template>

<style lang="less"></style>