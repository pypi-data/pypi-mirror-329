<script setup>
import { computed } from 'vue';


const emits = defineEmits(['change', 'update:modelValue'])

const props = defineProps({
    modelValue: {
        default: "",
    },
    placeholder: {
        type: String,
        default: "",
    },
    type: {
        type: String,
        default: "text",
    },
    disabled: {
        default: false,
    },
    width: {
        default: 100,
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
    <el-input class="xl-input xl-form-item" v-model="value" :placeholder="placeholder" :type="type" :disabled="disabled"
        :style="{ width: `${width}px` }"></el-input>
</template>


<style scoped>
.xl-input {}
</style>