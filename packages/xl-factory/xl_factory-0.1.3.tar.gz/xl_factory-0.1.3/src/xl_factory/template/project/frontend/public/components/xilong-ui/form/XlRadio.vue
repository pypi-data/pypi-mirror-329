<script setup>
import { computed } from 'vue';


const emits = defineEmits(['change', 'update:modelValue'])

const props = defineProps({
    modelValue: {
        type: String,
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
    <el-radio-group class="xl-radio" v-model="value">
        <el-radio v-for="(option, index) in options" :key="index" :label="option.value">{{ option.label
            }}</el-radio>
    </el-radio-group>
</template>


<style lang="less"></style>