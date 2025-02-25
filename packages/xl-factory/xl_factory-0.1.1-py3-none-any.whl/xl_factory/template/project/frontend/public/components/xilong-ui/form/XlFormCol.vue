<script setup>
const props = defineProps({
    span: {},
    l: {},
    p: {}
})
</script>

<template>
    <el-col :span="span">
        <el-form-item :label="l" :prop="p">
            <slot />
        </el-form-item>
    </el-col>
</template>

<style lang="less"></style>