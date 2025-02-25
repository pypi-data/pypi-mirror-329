<script setup>
import { computed } from 'vue'


const emits = defineEmits(['change', 'update:modelValue'])

const props = defineProps({
    tmp: {
        type: Number,
        default: 0,
    },
    options: {
        type: Array,
        default: () => [],
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
    <el-tabs class="xl-menu-tab" v-model="value">
        <el-tab-pane v-for="(option, index) in options" :key="index" :label="option.label" :name="option.value">
        </el-tab-pane>
    </el-tabs>
</template>
  
  
<style lang="less" scoped>
.el-tabs__nav-wrap {
    padding-left: 10px;
}

.el-tabs__header {
    margin: 0 !important;
}
</style>