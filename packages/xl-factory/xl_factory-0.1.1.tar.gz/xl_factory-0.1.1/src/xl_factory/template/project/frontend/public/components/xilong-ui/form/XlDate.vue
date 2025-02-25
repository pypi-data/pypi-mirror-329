<script setup>
import { computed } from 'vue';


const props = defineProps({
    placeholder: {
        type: String,
        default: "选择日期",
    },
    disabled: {
        type: Boolean,
        default: false,
    },
    tmp: {
        type: String,
        default: "",
    },
    width: {
        default: 100,
    },
});

const emits = defineEmits(['change'])

const value = computed({
    get() {
        return props.tmp;
    },
    set(data) {
        emits('change', data)
    },
});
</script>


<template>
    <el-date-picker class="xl-date xl-form-item" type="date" :placeholder="placeholder" format="YYYY-MM-DD"
        value-format="YYYY-MM-DD" v-model="value" :disabled="disabled" clearable :style="{ width: `${width}px` }" />
</template>


<style lang="less">
.xl-date {
    .el-input__prefix {
        display: none !important;
    }
}
</style>