<script setup>
const emits = defineEmits('click')

const props = defineProps({
    disabled: {},
    loading: {},
    icon: {},
    l: {}
});
</script>

<template>
    <xl-button type="primary" v-bind="$props" @click="() => emits('click')">
        <el-icon>
            <Edit />
        </el-icon>
    </xl-button>
</template>

<style lang="less"></style>