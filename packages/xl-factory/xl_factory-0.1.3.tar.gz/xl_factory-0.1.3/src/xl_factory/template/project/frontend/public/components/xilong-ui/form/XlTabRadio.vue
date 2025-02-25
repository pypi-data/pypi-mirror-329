<script setup>
import { computed } from 'vue';


const emits = defineEmits(['change', 'update:modelValue'])

const props = defineProps({
    modelValue: {
        default: "",
    },
    options: {
        type: Array,
        default() {
            return [];
        },
    },
})

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
    <el-radio-group class="xl-tab-radio" v-model="value">
        <el-radio-button v-for="(option, index) in options" :key="index" :label="option.value">{{ option.label
            }}</el-radio-button>
    </el-radio-group>
</template>


<style lang="less">
.xl-tab-radio {}
</style>