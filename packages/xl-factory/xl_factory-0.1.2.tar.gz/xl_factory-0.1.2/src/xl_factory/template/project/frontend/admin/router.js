import { createRouter, createWebHistory } from 'vue-router';
import store from '@/js/store'


const routes = []

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            redirect: '/login',
        },
        ...routes
    ],
});

router.beforeEach((to, from, next) => {
    // 添加标签页
    if (to.meta.title) {
        store.addTab({
            title: to.meta.title,
            path: to.path,
            name: to.name,
            query: to.query,
            params: to.params
        })
    }
    next()
})

export default router;