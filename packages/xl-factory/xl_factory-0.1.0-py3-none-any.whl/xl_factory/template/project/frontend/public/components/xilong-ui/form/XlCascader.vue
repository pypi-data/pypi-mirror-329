<script setup>
import { computed } from 'vue';


const props = defineProps({
    tmp: {
        type: String,
        default: "",
    },
    options: {
        type: Array,
        default() {
            return [];
        },
    },
    placeholder: {
        type: String,
        default: "",
    },
    width: {
        default: 300,
    },
})

const emits = defineEmits(['change'])

const value = computed({
    get() {
        return props.tmp.split("/");
    },
    set(data) {
        emits('change', data.join("/"));
    },
});
</script>


<template>
    <el-cascader class="xl-cascader" v-model="value" :options="options" :placeholder="placeholder"
        :style="{ width: width + 'px' }"></el-cascader>
</template>


<style></style>