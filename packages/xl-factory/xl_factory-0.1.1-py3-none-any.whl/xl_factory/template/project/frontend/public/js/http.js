import axios from 'axios'
import { ElMessage } from 'element-plus';
import { inject } from 'vue'


const store = inject('store')
const http = axios.create({})


const setRequestToken = (config) => {
    const token = localStorage.getItem('accessToken')
    if (token) {
        config.headers['token'] = token
    }
    return config
}

http.interceptors.request.use(
    config => setRequestToken(config),
    () => { }
)

const handleResponseError = (response) => {
    if (response.status !== 200) {
        console.error('系统错误')
        return
    }
    const { code } = response.data
    switch (code) {
        case 401:
            ElMessage.error('您的登录状态已过期，请重新登录！')
            window.location.href = '/login'
            store.setAccessToken(null)
            store.setUserInfo({})
            break
    }
}

http.interceptors.response.use(
    (response) => {
        handleResponseError(response)
        return response
    },
    () => { }
)

const get = url => (params => http.get(url, { params }));
const post = url => (data => http.post(url, data));


const makeBlobUrl = obj => {
    return URL.createObjectURL(obj);
}

const getBlobUrl = url => (async params => {
    const res = await http.get(url, { params, responseType: 'blob' })
    return makeBlobUrl(res.data)
})

const downloadByBlob = url => (async (params, filename) => {
    const res = await http.get(url, { params, responseType: 'blob' })
    const { data } = res
    const link = document.createElement("a");
    link.download = filename;
    link.style.display = "none";
    link.href = makeBlobUrl(data)
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
})

const request = async (method, url, params) => {
    const response = await http.request({
        method: method,
        url: url,
        data: method === 'POST' || method === 'PUT' || method === 'PATCH' ? params : null,
        params: method === 'GET' || method === 'DELETE' ? params : null
    });
    const { status, data } = response
    if (status == 200) {
        if (data.code == 200) {
            return data.data
        } else {
            return data
        }
    }
}

const createRequest = (url) => {
    return {
        async get(params) {
            const data = await request('GET', url, params)
            return data
        },
        async getBlob(params) {
            const data = await http.get(url, { params, responseType: 'blob' })
            return data
        },
        async post(data, operation = '操作') {
            // console.log('post~')
            try {
                const rsp = await request('POST', url, data)
                if (rsp && rsp.code == 500) {
                    ElMessage.error(`${operation}失败:${rsp.msg}`)
                } else {
                    if (operation) {
                        ElMessage.success(`${operation}成功`)
                    }
                }
                return rsp
            } catch (e) {
                if (operation) {
                    ElMessage.error(`${operation}失败:${e}`)
                }
            }
        },
        async put(data, operation = '修改') {
            try {
                const rsp = await request('PUT', url, data)
                if (rsp && rsp.code == 500) {
                    ElMessage.error(`${operation}失败:${rsp.msg}`)
                } else {
                    if (operation) {
                        ElMessage.success(`${operation}成功`)
                    }
                }
                return rsp
            } catch (e) {
                if (operation) {
                    ElMessage.error(`${operation}失败:${e}`)
                }
            }
        },
        async del(params, operation = '删除') {
            try {
                const rsp = await request('DELETE', url, params)
                if (rsp && rsp.code == 500) {
                    ElMessage.error(`${operation}失败:${rsp.msg}`)
                } else {
                    if (operation) {
                        ElMessage.success(`${operation}成功`)
                    }
                }
                return rsp
            } catch (e) {
                if (operation) {
                    ElMessage.error(`${operation}失败:${e}`)
                }
            }
        }
    };
}

export { createRequest }