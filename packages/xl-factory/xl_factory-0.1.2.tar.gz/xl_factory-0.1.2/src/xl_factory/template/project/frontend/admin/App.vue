<script setup>
import TopBar from '@/components/TopBar.vue'
import SideBar from '@/components/SideBar.vue'
import router from './router'
import Dict from '#/main/system/dict'
import { path } from '@/js/route.js'
import { inject, onMounted } from 'vue'


// 注入全局状态管理
const store = inject('store')

/**
 * 身份验证和路由处理
 * 检查登录状态并进行相应路由跳转
 */
const authenticate = async () => {
  const token = localStorage.getItem('accessToken')
  await router.isReady()

  // 如果在登录页则登出
  if (path.value === '/login') {
    store.logout()
    return
  }

  // 验证token并处理路由
  if (token === '999999') {
    store.setMode(1)
    if (path.value === '/') {
      router.push('/dashboard')
    }
  } else {
    store.logout()
    router.push('/login')
  }
}

// 组件挂载后执行初始化
onMounted(async () => {
  await authenticate()
  Dict.getStatic()
})
</script>

<template>
  <!-- 用户视图 -->
  <div class="user-view" v-if="store.state.mode">
    <SideBar />
    <div class="body">
      <TopBar />
      <router-view  class="content" v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </div>
  </div>

  <!-- 系统视图 -->
  <div class="system-view" v-else>
    <router-view />
  </div>
</template>

<style lang="less">
// 导入全局样式
@import "@/css/iconfont/iconfont.css";
@import "@/css/reset.less";
@import "@/css/public.less";

// 全局背景样式
body {
  background: radial-gradient(circle at 10% 20%, rgb(0, 93, 133) 0%, rgb(0, 181, 149) 90%) !important;
}

// 基础布局样式
html,
body,
#app,
.user-view,
.system-view {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  max-width: none;
  text-align: left;
  color: #000;
}

// 用户视图布局
.user-view {
  display: flex;
  flex-flow: row;

  // 侧边栏样式
  .xl-side-bar {
    width: 150px;

    .logo-wrapper {
      display: flex;
      align-items: center;
      justify-content: center;
      padding-top: 5px;
      border-bottom: 1px solid #1c3b64;

      .logo {
        opacity: 0.9;
      }
    }
  }

  // 主体内容区样式
  .body {
    flex-grow: 1;
    height: 100%;
    width: 100%;
    display: flex;
    flex-flow: column;
    overflow-x: scroll;

    .content {
      background: #fff;
      flex-grow: 1;
      display: flex;
      flex-flow: column;
      border-radius: 5px;
      margin-right: 5px;
      overflow: hidden;
    }
  }
}
</style>