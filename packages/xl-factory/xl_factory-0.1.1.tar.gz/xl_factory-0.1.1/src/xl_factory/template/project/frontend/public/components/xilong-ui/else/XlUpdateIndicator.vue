<script setup>
import { computed } from 'vue'


const props = defineProps({
    state: {
        type: Object,
        default() {
            return {}
        },
    },
})

const formatDatetime = date =>
    `${date.getFullYear()}-` +
    `${("0" + (date.getMonth() + 1)).slice(-2)}-` +
    `${("0" + date.getDate()).slice(-2)} ` +
    `${("0" + date.getHours()).slice(-2)}:` +
    `${("0" + date.getMinutes()).slice(-2)}:` +
    `${("0" + date.getSeconds()).slice(-2)}`;

const text = computed(() => {
    const { lastUpdateTime } = props.state
    return lastUpdateTime ? `上次保存时间 ${formatDatetime(lastUpdateTime)}` : "";
})
</script>


<template>
    <span class="xl-update-indicator">{{ props.state.saving ? "保存中..." : text }}</span>
</template>


<style lang="less">
.xl-update-indicator {
    color: grey;
    font-size: 10px;
    margin-right: 15px;
}
</style>