<script setup>
const props = defineProps({
    index: {
        type: Number,
        default: 0,
    },
    data: {
        type: Object,
        default() {
            return {};
        },
    },
})
</script>


<template>
    <span :class="['z-status-indicator', data[index].class]">{{
        data[index].text
    }}</span>
</template>

  
<style lang="less">
.z-status-indicator {
    margin-right: 15px;

    &.red {
        color: red;
    }

    &.blue {
        color: blue;
    }

    &.green {
        color: green;
    }
}
</style>