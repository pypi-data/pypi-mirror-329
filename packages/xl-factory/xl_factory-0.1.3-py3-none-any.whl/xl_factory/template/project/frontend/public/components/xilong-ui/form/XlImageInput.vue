<script setup>
import { ref, computed } from 'vue'
import { compress } from 'image-conversion'


const emits = defineEmits(['change', 'update:modelValue'])

const props = defineProps({
    modelValue: {
        default: "",
    },
    api: {
        type: Function,
        default: () => ({})
    },
    width: {
        default: 635
    },
    height: {
        default: 750
    },
    headers: {
        type: Object,
        default: () => ({})
    },
    params: {
        type: Object,
        default: () => ({})
    },
    disabled: {
        type: Boolean,
        default: false,
    },
    compress: {
        default: 0,
    },
    accept: {
        type: String,
        default: ''
    },
})


const value = computed({
    get() {
        return props.modelValue;
    },
    set(data) {
        emits('change', data)
        emits('update:modelValue', data)
    },
});


const loading = ref(false)


function beforeUpload() {
    loading.value = true
}

function onSuccess(data, file, filelist) {
    loading.value = false;
    emits('update:modelValue', data)
}

async function upload(option) {
    let formData = new FormData();
    const { api, params } = props
    let { file } = option

    if (props.compress) {
        const res = await compress(file, props.compress)
        file = new File([res], file.name, { lastModified: Date.now() })
    }

    formData.append("file", file);
    formData.append("filename", file.name);
    for (let key in params) {
        formData.append(key, params[key]);
    }
    return api(formData);
}
</script>


<template>
    <el-upload class="xl-image-input" action="" v-loading="loading" :headers="headers" :http-request="upload"
        :before-upload="beforeUpload" :on-success="onSuccess" :show-file-list="false" :disabled="disabled"
        :accept="props.accept">
        <img v-if="value" class="image" :src="`https://storage.heinz97.top/${value}`"
            :style="`max-width: ${width}px;max-height:${height}px`" />
        <el-icon v-else class="icon" :style="`width: ${width}px;height:${height}px`">
            <Plus />
        </el-icon>
    </el-upload>
</template>
  
  
<style lang="less">
.xl-image-input {

    .el-upload {
        border: 1px dashed var(--el-border-color);
        border-radius: 6px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
        transition: var(--el-transition-duration-fast);

        &:hover {
            border-color: var(--el-color-primary);
        }
    }

    .image {
        display: block;
    }

    .el-icon.icon {
        font-size: 28px;
        color: #8c939d;
        text-align: center;
    }
}
</style>
