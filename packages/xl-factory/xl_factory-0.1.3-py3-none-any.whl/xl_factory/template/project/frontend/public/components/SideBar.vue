<script setup>
import { computed } from 'vue'
import { useRouter } from "vue-router";

// 路由实例
const router = useRouter();

// 菜单配置数据
const menuConfig = [
    {
        name: '数据中心',
        path: '/dashboard'
    },
    {
        name: '市场推广',
        path: '/market'
    },
    {
        name: '客户管理',
        children: [
            {
                name: '客户列表', 
                path: '/client'
            },
            {
                name: '客户记录',
                path: '/client/log'
            }
        ]
    },
    {
        name: '合同管理',
        path: '/contract'
    },
    {
        name: '资产管理', 
        path: '/asset'
    },
    {
        name: '文章管理',
        children: [
            {
                name: '技术文章',
                path: '/article/technology'
            },
            {
                name: '产品文章',
                path: '/article/product'
            },
            {
                name: '营销文章',
                path: '/article/marketing'
            },
            {
                name: '企管文章',
                path: '/article/management'
            }
        ]
    }
];

// 计算属性返回菜单配置
const menu = computed(() => menuConfig);

// 菜单项选择处理
const handleMenuItemSelect = (path) => {
    router.push(path);
};
</script>

<template>
    <xl-side-bar 
        :menu-items="menu"
        :default-openeds="['1', '2', '3', '4', '5', '6']"
        @select="handleMenuItemSelect"
    >
        <div class="logo-wrapper">
            <img 
                class="logo" 
                src="@/img/trademark.png" 
                alt="Element logo"
            />
        </div>
    </xl-side-bar>
</template>

<style lang="less" scoped>
.logo-wrapper {
    padding: 0 !important;

    .logo {
        height: 50px;
        width: 100% !important;
    }
}
</style>