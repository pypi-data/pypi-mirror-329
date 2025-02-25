<template>
    <div class="xl-image-viewer">
        <el-image :src="props.url" fit="scale-down" @click="handleClick"></el-image>
        <xl-image-preview-dialog ref="previewerRef" :url="props.url"></xl-image-preview-dialog>
        <!-- <el-image :src="props.url" @click="handleClick">
            <template #error class="image-slot">
                <el-icon>
                    <Picture />
                </el-icon>
            </template>
</el-image> -->
        <!-- <el-image fit="scale-down" :src="props.url" @click="handleClick">
            <template #error class="image-slot">
                <el-icon>
                    <Picture />
                </el-icon>
            </template>
        </el-image>
        <xl-image-preview-dialog ref="previewerRef" :url="props.url"></xl-image-preview-dialog> -->
    </div>
</template>

<script setup>
import { ref } from 'vue'


const props = defineProps({
    url: {
        type: String,
        default: "",
    },
})


const previewerRef = ref(null)


function handleClick() {
    previewerRef.value.show()
}
</script>

<style lang="less">
.xl-image-viewer {
    width: 100%;
    height: 100%;
    overflow: hidden;

    .el-dialog__header {
        display: none;
    }

    .el-image {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
}
</style>