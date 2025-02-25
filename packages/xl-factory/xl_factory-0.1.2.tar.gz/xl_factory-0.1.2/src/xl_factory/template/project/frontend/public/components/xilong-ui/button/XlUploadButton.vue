<script setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus'


const emits = defineEmits(['uploaded'])

const props = defineProps({
    api: {
        type: Function,
        default: () => { },
    },
    params: {
        type: Object,
        default() {
            return {};
        },
    },
    text: {
        type: String,
        default: "上传",
    },
    allowedTypes: {
        type: Array,
        default() {
            return [];
        },
    },
    disabled: {
        type: Boolean,
        default: false,
    },
    type: {
        type: String,
        default: "",
    },
})

const headers = { token: localStorage.getItem("accessToken") }
const loading = ref(false)

const handlers = {
    validateFileType(fileType) {
        const { allowedTypes } = props;
        if (allowedTypes.length == 0) {
            return true;
        } else {
            if (allowedTypes.indexOf(fileType) < 0) {
                return false;
            } else {
                return true;
            }
        }
    },
    beforeUpload(file) {
        loading.value = true;
    },
    upload(option) {
        const { params } = props
        let formData = new FormData();
        const file = option.file;
        const filename = file.name;
        const fileType = file.type;
        if (!handlers.validateFileType(fileType)) {
            ElMessage.error(`文件类型错误`)
            loading.value = false;
            return;
        }
        formData.append("file", file);
        formData.append("file_name", filename);
        for (let key in params) {
            formData.append(key, params[key]);
        }
        return props.api(formData);
    },
    onSuccess(data, file, filelist) {
        loading.value = false;
        emits("uploaded", data);
    },
}
</script>


<template>
    <el-upload class="xl-upload-button" ref="uploader" action="" :headers="headers" :http-request="handlers.upload"
        :before-upload="handlers.beforeUpload" :on-success="handlers.onSuccess" :show-file-list="false"
        :disabled="disabled">
        <xl-button :loading="loading" :type="type">
            <slot />
        </xl-button>
    </el-upload>
</template>


<style lang="less">
.xl-upload-button {
    display: inline-block;

    .el-upload {
        display: inline-block;
    }
}
</style>
