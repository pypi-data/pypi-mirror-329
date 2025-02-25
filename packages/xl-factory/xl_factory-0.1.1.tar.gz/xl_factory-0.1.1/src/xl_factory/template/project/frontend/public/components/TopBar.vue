<script setup>
import { inject } from 'vue'

// 注入全局状态管理
const store = inject('store')

// 退出登录处理函数
const handleLogout = () => {
    store.logout()
}
</script>

<template>
    <el-menu 
        class="top-bar" 
        :default-active="activeIndex" 
        mode="horizontal" 
        :ellipsis="false"
    >
        <div style="flex: 1;justify-content: left;">
            <xl-tabs-nav />
        </div>
        <div>
            <xl-button @click="handleLogout">退出</xl-button>
        </div>
    </el-menu>
</template>

<style lang="less">
// 顶部导航栏样式
.top-bar {
    height: 50px;
    text-align: right;
    display: flex;
    justify-content: right;
    align-items: center;
    margin: 5px 5px 5px 0 !important;
    padding-right:20px;
    border-radius: 5px;
    background: rgb(0 0 0 / 40%) !important;

    .div:nth-of-type(1){
    padding: 0!important;
  }
}

// Element Plus 菜单主题变量覆盖
:root {
    --el-menu-text-color: rgb(102, 102, 102) !important;
    --el-menu-active-color: rgb(58, 111, 163) !important;
    --el-menu-hover-text-color: rgb(58, 111, 163) !important;
    --el-menu-hover-bg-color: #fff !important;
}
</style>