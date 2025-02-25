<script setup>
const props = defineProps({
    l: {},
    p: {}
})
</script>

<template>
    <el-row>
        <el-col :span="24">
            <el-form-item :label="l" :prop="p">
                <slot />
            </el-form-item>
        </el-col>
    </el-row>
</template>

<style lang="less"></style>