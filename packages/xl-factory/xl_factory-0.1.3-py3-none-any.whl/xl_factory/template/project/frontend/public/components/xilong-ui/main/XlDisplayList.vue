<script setup>
import { inject } from 'vue'


const props = defineProps({
    selectable: {
        type: Boolean,
        default: false,
    },
    showSummary: {
        type: Boolean,
        default: false,
    },
    rowClick: {
        type: Function,
        default: () => { },
    },
    summaryMethod: {
        type: Function,
        default: () => { },
    },
    showIndex: {
        type: Boolean,
        default: true,
    },
    pagination: {
        type: Object,
        default() {
            return {
                pageNum: 1,
                pageSize: 20,
                total: 0,
            };
        },
    },
    spanMethod: {
        type: Function,
        default: () => { },
    },
    headerCellStyle: {
        type: Function,
        default: () => { },
    },
    rowClassName: {
        type: Function,
        default: () => { },
    },
    rowKey: {
        type: Function,
        default: () => { },
    },
    rowDblClick: {
        type: Function,
        default: () => { },
    },
    selectionChange: {
        type: Function,
        default: () => { },
    },
    layout: {
        type: String,
        default: 'prev, pager, next, jumper'
    },
    small: {
        type: Boolean,
        default: false
    },
    type: {
        type: String,
        default: ''
    },
    width: {
        default: 70
    },
    labelWidth: {
        default: 90
    },
    callback: {
        type: Function,
        default: () => { },
    },
});

const { refs, api, params, obj, ruleMap, chartOptions } = inject('injections')

try {
    api.stat()
} catch (error) {
    console.error(error)
}
</script>


<template>
    <div class="xl-display-list">
        <xl-query-control :type="type" :table="refs.table" :params="params" @query="() => api.stat()">
            <template #inputs>
                <slot name="inputs" />
            </template>
            <template #buttons>
                <slot name="buttons" />
            </template>
        </xl-query-control>
        <xl-query-page-table v-show="params.view != 'chart'" :ref="refs.table" :api="api" :params="params"
            v-bind="$props" :sort-change="(data) => api.sort(data)">
            <slot name="columns" />
        </xl-query-page-table>
        <xl-chart v-show="params.view == 'chart'" :options="chartOptions" />
        <slot name="others" />
    </div>
</template>


<style lang="less">
.xl-display-list {
    div.cell {
        padding: 0 !important;

    }
}
</style>