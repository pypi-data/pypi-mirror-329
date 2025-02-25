import { computed } from 'vue'

// URL参数解析工具函数
const getUrlParam = (paramName) => {
    const urlParams = new URLSearchParams(window.location.search)
    return urlParams.get(paramName)
}

// 路由相关的计算属性
const path = computed(() => window.location.pathname)

const articleId = computed(() => getUrlParam('articleId'))

const clientId = computed(() => getUrlParam('clientId'))

// 在当前窗口跳转
const jump = (path) => {
    window.location.href = path
}

// 在新窗口打开
const open = (path) => {
    window.open(path, '_blank')
}

export {
    path,
    articleId,
    clientId,
    jump,
    open
}
