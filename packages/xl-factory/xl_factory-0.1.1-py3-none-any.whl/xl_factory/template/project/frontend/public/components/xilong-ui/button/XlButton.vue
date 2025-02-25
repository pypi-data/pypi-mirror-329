<script setup>
const props = defineProps({
    type: {},
    disabled: {},
    loading: {},
    icon: {},
    l: {}
});
</script>


<template>
    <el-button class="xl-button" :type="type" :disabled="disabled" :loading="loading" :icon="icon">
        <span v-if="l">{{ l }}</span>
        <slot />
    </el-button>
</template>


<style lang="less"></style>