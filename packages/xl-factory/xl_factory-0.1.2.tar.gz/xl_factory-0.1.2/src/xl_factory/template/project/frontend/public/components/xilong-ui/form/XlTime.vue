<script setup>
import { computed } from 'vue';


const emits = defineEmits(['change', 'update:modelValue'])

const props = defineProps({
    modelValue: {
        default: "",
    },
    placeholder: {
        type: String,
        default: "选择时间",
    },
    disabled: {
        type: Boolean,
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
    <el-date-picker class="xl-time xl-form-item" v-model="value" type="datetime" :placeholder="placeholder"
        :style="{ width: `${width}px` }" :disabled="disabled" clearable value-format="YYYY-MM-DD HH:mm:ss" />
</template>


<style lang="less">
.z-time {
    .el-input__prefix {
        display: none !important;
    }
}
</style>