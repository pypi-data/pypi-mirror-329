import { reactive } from 'vue'
import storage from './storage.js'

class Store {
    constructor() {
        // 初始化响应式状态
        this.state = reactive(this.getDefaultState())
    }

    // 获取默认状态
    getDefaultState() {
        return {
            accessToken: storage.get('accessToken'),
            mode: 0,
            topBarIndex: '0',
            // 添加标签页管理相关状态
            tabs: [],
            activeTab: ''
        }
    }
    // 添加标签页
    addTab(tab) {
        // 如果标签页不存在才添加
        if (!this.state.tabs.find(t => t.path === tab.path)) {
            this.state.tabs.push({
                title: tab.title,
                path: tab.path,
                name: tab.name,
                query: tab.query || {},
                params: tab.params || {}
            })
        }
        this.state.activeTab = tab.path
    }

    // 关闭标签页
    closeTab(path, router) {
        const index = this.state.tabs.findIndex(tab => tab.path === path)
        if (index === -1) return

        // 如果关闭的是当前激活的标签页，需要激活其他标签页
        if (this.state.activeTab === path) {
            if (this.state.tabs.length > 1) {
                // 优先激活右侧标签，没有则激活左侧标签
                const nextTab = this.state.tabs[index + 1] || this.state.tabs[index - 1]
                this.state.activeTab = nextTab.path
                router.push(nextTab.path)
            }
        }

        this.state.tabs.splice(index, 1)
    }

    // 设置当前激活的标签页
    setActiveTab(path) {
        this.state.activeTab = path
    }


    // 设置模式
    setMode(mode) {
        this.state.mode = mode
    }

    // 重置状态
    reset() {
        Object.assign(this.state, this.getDefaultState())
    }

    // 登出操作
    logout() {
        localStorage.clear()
        this.reset()
    }
}

export default new Store()
