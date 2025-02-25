<script setup>
import { inject } from 'vue'


const props = defineProps({
    control: {},
    table: {},
    addDialog: {},
    editDialog: {},
})

const { refs, api, params, chartOptions } = inject('injections')

try {
    api.stat()
} catch (error) {
    console.error(error)
}
</script>


<template>
    <div class="list">
        <component :is="control" />
        <component :is="table" v-show="params.view != 'chart'" />
        <xl-chart v-show="params.view == 'chart'" :options="chartOptions" />
        <component :is="addDialog" />
        <component :is="editDialog" />
        <xl-message-dialog :ref="refs.deleteDialog" message="是否确认删除？" @confirm="() => api.delete()" />
    </div>
</template>


<style lang="less"></style>