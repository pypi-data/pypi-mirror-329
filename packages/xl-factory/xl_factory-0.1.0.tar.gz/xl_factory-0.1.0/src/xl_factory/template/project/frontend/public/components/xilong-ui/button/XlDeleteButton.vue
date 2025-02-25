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
    <xl-button type="danger" v-bind="$props" @click="() => emits('click')">
        <el-icon>
            <Delete />
        </el-icon>
    </xl-button>
</template>

<style lang="less"></style>