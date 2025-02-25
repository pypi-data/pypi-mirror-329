<script setup>
import { ref } from 'vue'


const props = defineProps({
    api: {
        type: Function,
        default: () => ({}),
    },
    disabled: {
        type: Boolean,
        default: false
    },
    type: {
        type: String,
    },
    width: {
        type: Number,
    },
    icon: {
        type: String,
        default: "",
    },
});


const btnRef = ref(null)
const loading = ref(false)

async function handleClick() {
    loading.value = true;
    try {
        await props.api();
        loading.value = false;
        setTimeout(() => {
            loading.value = false;
        }, 450);
    } catch (e) {
        loading.value = false;
    }
}

function click() {
    btnRef.value.$el.click()
}

defineExpose({ click })
</script>


<template>
    <el-button class="xl-button xl-async-button" ref="btnRef" :type="type" :disabled="disabled" :loading="loading"
        :icon="icon" @click="handleClick">
        <span v-if="!loading">
            <slot />
        </span>
    </el-button>
</template>


<style></style>