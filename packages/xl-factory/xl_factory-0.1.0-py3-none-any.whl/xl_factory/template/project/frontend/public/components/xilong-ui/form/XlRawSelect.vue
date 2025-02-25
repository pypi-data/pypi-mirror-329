<script setup>
import { ref, computed } from 'vue';


const emits = defineEmits(['change', 'update:modelValue'])

const props = defineProps({
    modelValue: {
        default: '',
    },
    labels: {
        type: Array,
        default: () => [],
    },
    disabled: {
        type: Boolean,
        default: false,
    },
    width: {
        default: 100,
    },
    multiple: {
        type: Boolean,
        default: false,
    },
    placeholder: {
        type: String,
        default: '',
    },
    allowCreate: {
        type: Boolean,
        default: false,
    },
});


const visible = ref(true)

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
    <el-select v-if="visible" class="xl-raw-select xl-form-item" v-model="value" :placeholder="placeholder"
        :disabled="disabled" :style="{ width: `${width}px` }" :multiple="multiple" clearable>
        <el-option v-for="(label, index) in labels" :key="index" :value="label">
            {{ label }}
        </el-option>
    </el-select>
</template>


<style lang="less" scoped>
.el-select {
    margin: 3px 0;
}

.el-input__inner {
    padding: 0 5px !important;
}
</style>
