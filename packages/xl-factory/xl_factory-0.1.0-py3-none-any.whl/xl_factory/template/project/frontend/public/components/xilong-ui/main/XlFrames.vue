<script setup>
import { ref, watch } from 'vue'


const emits = defineEmits(['change'])

const props = defineProps({
    index: {
        type: Number,
        default: 0,
    },
    frames: {
        type: Array,
        default: () => [],
    },
    data: {
        type: Object,
    }
})


const tabIndex = ref(props.index + '')


watch(tabIndex, (val) => {
    emits('change', val)
})
</script>


<template>
    <div class="xl-frames">
        <el-tabs class="xl-menu-tab" v-model="tabIndex">
            <el-tab-pane v-for="(frame, index) in props.frames" :key="index" :label="frame.label" :name="`${index}`">
            </el-tab-pane>
        </el-tabs>
        <component class="frame" v-for="(frame, index) in frames" :key="index" v-show="tabIndex == index"
            :is="frame.entity" :tab-index="tabIndex" :data="data"></component>
    </div>
</template>


<style lang="less">
.xl-frames {

    display: flex;
    flex-flow: column;
    flex-grow: 1;
    position: relative;
    background: #fff;
    color: #000;

    .xl-menu-tab {
        height: 40px;

        .el-tabs__nav-wrap {
            padding-left: 10px;
        }

        .el-tabs__header {
            margin: 0 !important;
        }
    }

    .frame {
        flex-grow: 1;
        overflow-y: scroll;
        display: flex;
        flex-flow: column;
    }
}
</style>