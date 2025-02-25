const set = (key, data) => {
    if (typeof (data) == 'object') {
        data = JSON.stringify(data)
    }
    localStorage.setItem(key, data)
}

const get = key => {
    let data = localStorage.getItem(key)
    if (data) {
        if (data.includes('{')) {
            data = JSON.parse(data)
        }
    }
    return data
}


export default {
    set, get
}