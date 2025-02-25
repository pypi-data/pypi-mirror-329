<template>
    <div class="tabs-nav">
      <div
        v-for="tab in store.state.tabs"
        v-ripple
        :key="tab.path"
        class="tab-item"
        :class="{ active: tab.path === store.state.activeTab }"
        @click="switchTab(tab)"
      >
        <span>{{ tab.title }}</span>
        <span class="close-icon" @click.stop="closeTab(tab.path)">&times;</span>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router'
  import store from '@/js/store.js'
  
  const router = useRouter()
  
  const switchTab = (tab) => {
    router.push(tab.path)
    store.setActiveTab(tab.path)
  }
  
  const closeTab = (path) => {
    store.closeTab(path, router)
  }
  </script>
  
  <style lang="less">
  .tabs-nav {
    display: flex;
    padding: 4px 4px 0;
  }
  

 
  .tab-item {
    height:20px;

    padding: 5px 10px;
    background: #fff;
    color:rgb(100,100,100);
    margin-right: 3px;
    // border: 1px solid #d9d9d9;
    /* border-bottom: none; */
    border-radius: 4px;
    cursor: pointer;
    display: flex;
    align-items: center;
    font-size: 14px;
    color:rgb(100,100,100);
    /* gap: 8px; */
  }
  
  .tab-item.active {
    background: rgb(66, 185, 131);
    color:#fff;
  }
  
  .close-icon {
    font-size: 14px;
    width: 16px;
    height: 16px;
    line-height: 16px;
    text-align: center;
    border-radius: 50%;
  }
  
  .close-icon:hover {
    background: #ccc;
  }
  
  .tabs-content {
    flex: 1;
    display: flex;
    flex-flow: column;
    overflow: auto;
  }
  </style>