<script setup>
import { onMounted, ref, computed, watch } from 'vue'


const emits = defineEmits(['change', 'update:modelValue'])

const props = defineProps({
    modelValue: {
        default: '',
    },
    options: {
        type: Array,
        default: [],
    },
    placeholder: {
        type: String,
        default: "",
    },
    disabled: {
        type: Boolean,
        default: false,
    },
    multiple: {
        type: Boolean,
        default: false,
    },
    width: {
        default: 100,
    },
})

const showOptions = ref([])

const value = computed({
    get() {
        return props.modelValue;
    },
    set(data) {
        emits('change', data)
        emits('update:modelValue', data)
    },
});

function handleClick() {
    showOptions.value = props.options;
}

function handleFilter(val) {
    if (val) {
        showOptions.value = props.options.filter((item) => {
            return item.label ? item.label.includes(val) : false;
        });
    } else {
        showOptions.value = props.options;
    }
}

watch(() => props.options, (val) => {
    handleClick()
})

onMounted(() => {
    handleClick()
})
</script>


<template>
    <el-select class="xl-search-select xl-form-item" v-model="value" :placeholder="placeholder" filterable
        :filter-method="handleFilter" @click="handleClick" :style="{ width: `${width}px!important` }"
        :disabled="disabled" :multiple="multiple" clearable>
        <el-option v-for="(option, index) in showOptions" :key="index" :label="option.label" :value="option.value">
        </el-option>
    </el-select>
</template>


<style></style>