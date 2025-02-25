<script setup>
import { ref } from 'vue'


const emits = defineEmits(['change', 'item-contextmenu'])

const props = defineProps({
    items: {
        type: Array,
        default: () => [],
    },
    name: {
        type: String,
        default: "label",
    },
    width: {
        default: 200,
    },
    loading: {
        default: false,
    },
})

const activeIndex = ref(0)


function handleClickItem(index, item) {
    activeIndex.value = index;
    emits('change', item)
}

function handleContextMenu(e, item) {
    emits('item-contextmenu', e, item)
}
</script>


<template>
    <div class="xl-items-bar" :style="{ width: `${width}px` }" v-loading="loading">
        <div class="item" v-for="(item, index) in items" :key="index" :class="{ active: activeIndex == index }"
            @click="handleClickItem(index, item)" @contextmenu="handleContextMenu($event, item)">
            <span :title="item[name]">{{ item[name] }}</span>
        </div>
    </div>
</template>


<style lang="less" scoped>
.xl-items-bar {
    font-size: 13px;
    border-right: 1px solid rgb(240, 240, 240);
    overflow-y: scroll;
    background: #fff;

    .active {
        background: rgb(26, 157, 255);
        color: rgb(240, 240, 240);
    }

    &>div {
        padding: 10px 7px;
        color: rgb(70, 100, 150);
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        cursor: pointer;
        text-align: left;
    }
}
</style>
