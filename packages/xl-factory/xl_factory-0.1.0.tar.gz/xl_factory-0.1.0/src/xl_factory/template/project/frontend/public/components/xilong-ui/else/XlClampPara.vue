<script setup>
const props = defineProps({
    text: {},
    lines: {
        type: Number,
        default: 1
    }
})
</script>

<template>
    <p :title="text" :style="`-webkit-line-clamp:${lines}`">
        {{ text }}
    </p>
</template>

<style lang="less" scoped>
p {
    overflow: hidden;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    text-align: left;
}
</style>