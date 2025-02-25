<script setup>
import { onMounted } from 'vue';


const emits = defineEmits(['query', 'clear'])

const props = defineProps({
    type: {},
    table: {},
    params: {
        type: Object,
        default: () => ({})
    },
});

const defaultFilter = { ...props.params }


const handlers = {
    query() {
        if (props.table) {
            props.table.value.query()
        }
        emits('query')
    },
    clear() {
        if (props.table) {
            reset(props.params, defaultFilter)
            props.table.value.query()
        }
        emits('clear')
    }
}

function reset(a, b) {
    for (const key in a) {
        delete a[key];
    }
    for (const key in b) {
        a[key] = b[key];
    }
}

onMounted(() => {
    props.params.view = 'table'
})
</script>


<template>
    <div class="xl-query-control">
        <el-radio-group v-if="type == 'view'" class="xl-radio" v-model="params.view">
            <el-radio-button label="table">
                <el-icon>
                    <Grid />
                </el-icon>
            </el-radio-button>
            <el-radio-button label="chart">
                <el-icon>
                    <TrendCharts />
                </el-icon>

            </el-radio-button>
        </el-radio-group>
        <div class="inputs" @keyup.enter="handlers.query">
            <slot name="inputs" />
            <xl-button class="query-btn" type="primary" @click="handlers.query">查询</xl-button>
            <xl-button class="reset-btn" @click="handlers.clear">重置</xl-button>
        </div>
        <div class="buttons">
            <slot name="buttons" />
        </div>
    </div>
</template>


<style lang="less">
.xl-query-control {
    display: flex;
    flex-flow: row;
    align-items: center;
    width: 100%;
    padding: 3px 0;
    background: #fff !important;

    .el-tabs__header {
        background: #fff !important;
    }

    .el-icon {
        font-size: 20px;
    }

    .el-radio-button__inner {
        padding: 4px 10px;
    }

    .inputs {
        text-align: left;

        >* {
            margin-right: 5px !important;
        }
    }

    .xl-radio {
        margin-right: 5px;
        margin-left: 3px;
    }

    .buttons {
        flex-grow: 1;
        padding: 0 5px;
        width: 150px;
        text-align: right;

        .xl-button {
            display: inline-block !important;
        }

        >* {
            margin-right: 5px !important;
        }
    }

    .el-button+.el-button {
        margin: 0;
    }
}
</style>