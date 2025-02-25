<script setup>
const emits = defineEmits(['change', 'update:modelValue'])

const props = defineProps({
    modelValue: {
        default: 0,
    },
    items: {
        type: Array,
        default: ()=>[]
    }
})

const handleClick = index => {
    emits('change', index)
    emits('update:modelValue', index)
}
</script>

<template>
  <div class="xl-menu-bar">
        <a v-for="item, index in items" :key="index" @click="handleClick(index)">
            <div>{{item.name}}</div>
        </a>
  </div>
</template>

<style lang="less">
.xl-menu-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    display: flex;
    width: 100%;
    height: 40px;
    line-height: 40px;
    border-top: 1px solid grey;
    background: #fff;

    a {
        flex: 1;
        cursor: pointer;
        border-right: 1px solid grey;

        div {
            color:#000;
            text-align: center;
        }
    }
}
</style>