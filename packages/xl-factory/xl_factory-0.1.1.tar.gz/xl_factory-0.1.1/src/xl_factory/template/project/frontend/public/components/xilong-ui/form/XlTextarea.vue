<script setup>
import { computed } from 'vue';


const emits = defineEmits(["update:modelValue", 'change']);

const props = defineProps({
    modelValue: {
    },
    placeholder: {
        type: String,
        default: "",
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
        emits("update:modelValue", data)
    },
});
</script>


<template>
    <el-input class="xl-textarea xl-form-item" v-model="value" :placeholder="placeholder" type="textarea" size="small"
        :disabled="disabled" :autosize="{ minRows: 2 }"></el-input>
</template>


<style lang="less" scoped>
textarea {
    width: 100%;
    height: 100%;
}
</style>