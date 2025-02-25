<script setup>
import { ref } from 'vue'

const props = defineProps({
    message: {
        type: String,
        default: "",
    },
});

const emits = defineEmits(['confirm', 'cancel'])


const visible = ref(false)

const onConfirm = () => {
    hide()
    emits('confirm')
}

const onCancel = () => {
    hide()
    emits('cancel')
}

const show = () => {
    visible.value = true
}

const hide = () => {
    visible.value = false
}


defineExpose({ show })
</script>


<template>
    <el-dialog class="xl-message-dialog xl-dialog" v-model="visible" title="提示" width="30%">
        <div class="message">
            <span>{{ message }}</span>
        </div>
        <div slot="footer" class="dialog-footer">
            <el-button @click="onCancel">否</el-button>
            <el-button type="primary" @click="onConfirm">是</el-button>
        </div>
    </el-dialog>
</template>
    
    
<style lang="less">
.xl-message-dialog {
    .el-dialog__header {
        text-align: left;
    }

    .message {
        text-align: left;
    }

    .dialog-footer {
        text-align: center;
        margin-top: 20px;
    }
}
</style>