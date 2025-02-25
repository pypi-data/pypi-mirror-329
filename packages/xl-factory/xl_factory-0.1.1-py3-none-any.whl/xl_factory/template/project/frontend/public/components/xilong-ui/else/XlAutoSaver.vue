<template>
    <div class="xl-auto-saver" @mouseleave="onBlur" @click="onClick">
        <slot />
    </div>
</template>


<script setup>
import { reactive } from 'vue'


const props = defineProps({
    api: {
        type: Function,
        default: async () => { }
    },
    disabled: {
        type: Boolean,
        default: false,
    },
})

const state = reactive({
    saving: false,
    lastUpdateTime: null
})


async function onBlur() {
    let { api, disabled } = props;
    if (disabled) {
        return;
    }
    state.saving = true;
    const code = await api();
    state.saving = false;
    if (code == 1) {
        state.lastUpdateTime = new Date();
    }
}

async function onClick() {
    const { api, disabled } = props;
    if (disabled) {
        return;
    }
    let now = new Date();
    let lapse = state.lastUpdateTime ? now - state.lastUpdateTime : 3500;
    if (lapse > 3000 && !state.saving) {
        state.saving = true;
        const code = await api();
        state.saving = false;
        if (code == 1) {
            state.lastUpdateTime = new Date();
        }
    }
}


defineExpose({
    state
})
</script>

<style lang="less">
.xl-auto-saver {
    display: flex;
    flex-flow: column;
}
</style>