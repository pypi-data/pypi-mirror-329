<script setup>
import { ref, computed } from 'vue';


const props = defineProps({
    tmp: {
        type: Array,
        default: () => [],
    },
    options: {
        type: Array,
        default: () => [],
    },
    max: {
        type: Number,
        default: 1,
    },
});


const emits = defineEmits(['change']);


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
    <el-checkbox-group class="xl-checkbox-group" v-model="value" :max="max">
        <el-checkbox class="xl-checkbox" v-for="(option, index) in options" :key="index" :label="option.value">{{
            option.label }}</el-checkbox>
    </el-checkbox-group>
</template>
    
    
<style></style>