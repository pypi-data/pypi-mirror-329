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
        default: false,
    },
    disableAdd: {
        type: Boolean,
        default: false,
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
    width: {
        default: 70
    },
    title: {
        type: String,
        default: ''
    },
    callback: {
        type: Function,
        default: () => { },
    },
});

const { refs, api, params, obj, ruleMap } = inject('injections')

try {
    api.stat()
} catch (error) {
    console.error(error)
}
</script>


<template>
    <div class="xl-chart-list">
        <xl-query-control type="view" :table="refs.table" :params="params" @query="() => api.getStat()">
            <template #inputs>
                <slot name="inputs" />
            </template>
            <template #buttons>
                <slot name="buttons" />
                <el-button class="add-btn" v-if="!disableAdd" type="success" @click="() => api.onAdd()">新增</el-button>
            </template>
        </xl-query-control>
        <xl-query-page-table v-show="params.view != 'chart'" :ref="refs.table" :api="api" :params="params"
            v-bind="$props" :sort-change="(data) => api.sort(data)">
            <slot name="columns" />
        </xl-query-page-table>
        <div class="charts" v-show="params.view == 'chart'">
            <slot name="charts" />
        </div>
        <xl-edit-dialog :ref="refs.editDialog" :title="title" :width="width" label-width="90" :data="obj"
            :rule-map="ruleMap" :callback="callback">
            <slot name="items" />
        </xl-edit-dialog>
        <slot name="others" />
        <xl-message-dialog :ref="refs.deleteDialog" message="是否确认删除？" @confirm="() => api.delete()" />
    </div>
</template>


<style lang="less">
.xl-chart-list {
    .charts {
        height: calc(~"100vh - 120px")
    }
}
</style>