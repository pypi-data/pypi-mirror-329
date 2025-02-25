<script setup>
import { ref } from 'vue';


const emits = defineEmits(['confirm', 'pass', 'reject', 'close'])

const props = defineProps({
    title: {
        type: String,
        default: "提示",
    },
    width: {
        default: 30,
    },
    validate: {
        type: Function,
        default() {
            return true
        }
    },
    passCallback: {
        type: Function,
        default: async () => 0
    },
    rejectCallback: {
        type: Function,
        default: async () => 0
    }
});

const visible = ref(false);

const onPass = async () => {
    const validation = await props.validate()
    if (validation) {
        emits('confirm');
        const error = await props.passCallback()
        if (!error) {
            hide();
            emits('pass');
        }
    }
};

const onReject = async () => {
    const error = await props.rejectCallback()
    if (!error) {
        hide();
        emits('reject');
    }
};

const onClose = () => {
    emits('close');
};

const show = () => {
    visible.value = true;
};

const hide = () => {
    visible.value = false;
};

defineExpose({ show })
</script>


<template>
    <el-dialog class="xl-review-dialog" :title="title" v-model="visible" @close="onClose" :width="width + '%'">
        <slot />
        <div style="text-align: center; padding: 10px; margin-top: 20px">
            <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="onPass">通过</el-button>
                <el-button type="danger" @click="onReject">驳回</el-button>
            </span>
        </div>
    </el-dialog>
</template>


<style lang="less">
.xl-review-dialog {
    text-align: left;

    border-radius: 10px 10px 7px 7px !important;
    padding: 0;

    .el-dialog__header {
        border-radius: 7px 7px 0 0;
        padding: 14px 20px 10px;
        background: transparent linear-gradient(90deg, #073052 0%, rgb(100, 100, 100) 100%) 0% 0% no-repeat padding-box !important;

        .el-dialog__headerbtn {
            top: 14px;
        }

        .el-dialog__title,
        .el-dialog__close {
            color: rgb(245, 245, 245) !important;
        }

        .el-dialog__headerbtn {
            top: 3px !important;
        }

    }

    .el-dialog__body {
        padding: 10px 10px 5px 10px;
    }
}
</style>