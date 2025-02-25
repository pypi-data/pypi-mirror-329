import App from './App.vue'
import store from '@/js/store'
import { ripple } from '@/directives/ripple'
import { createApp } from 'vue'


const app = createApp(App)

// 路由
import router from './router';
app.use(router);

app.directive('ripple', ripple)

// 状态管理
app.provide('store', store)

// element-plus
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
app.use(ElementPlus);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

import HighchartsVue from 'highcharts-vue'
import Highcharts from 'highcharts';
Highcharts.setOptions({
    xAxis: {
        dateTimeLabelFormats: {
            millisecond: "%H:%M:%S.%L",
            second: "%H:%M:%S",
            minute: "%H:%M",
            hour: "%H:%M",
            day: "%m-%d",
            week: "%m-%d",
            month: "%Y-%m",
            year: "%Y",
        },
    },
    credits: {
        enabled: false,
    },
})
app.use(HighchartsVue);
Highcharts.seriesTypes.line.prototype.getPointSpline = Highcharts.seriesTypes.spline.prototype.getPointSpline;


// XilongUI
import XilongUI from '@/components/xilong-ui'
app.use(XilongUI);

import xilonguimain from '@xilonglab/xl-ui-main'
app.use(xilonguimain);

import xilonguitable from '@xilonglab/xl-ui-table'
app.use(xilonguitable);

import xilonguichart from '@xilonglab/xl-ui-chart'
app.use(xilonguichart);

app.mount('#app')


