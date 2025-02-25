<script setup>
import { computed } from 'vue';


const emits = defineEmits(['change', 'update:modelValue'])

const props = defineProps({
    modelValue: {
        type: Number,
        default: 0,
    },
});

const value = computed({
    get() {
        return props.modelValue;
    },
    set(data) {
        emits('change', data)
        emits('update:modelValue', data)
    },
});
</script>


<template>
    <el-switch class="xl-switch" v-model="value" :active-value="1" :inactive-value="0" />
</template>


<style lang="less" scoped></style>