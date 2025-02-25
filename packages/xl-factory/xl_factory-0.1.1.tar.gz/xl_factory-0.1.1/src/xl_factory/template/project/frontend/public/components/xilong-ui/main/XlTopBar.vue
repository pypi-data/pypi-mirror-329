<script setup>
</script>


<template>
    <div class="xl-top-bar">
        <el-col :span="12" class="left">
            <slot name="left" />
        </el-col>
        <el-col :span="12" class="right">
            <slot name="right" />
        </el-col>
    </div>
</template>


<style lang="less">
.xl-top-bar {
    position: relative;
    width: 100%;
    height: 59px;
    background: #fff;
    color: #000;
    display: flex;
    align-items: center;
    box-shadow: 0 1px 4px rgb(222, 222, 222, 0.08);

    .left {
        display: flex;
        align-items: center;
        font-size: 18px;
        padding-left: 10px;
    }

    .right {
        display: flex;
        justify-content: flex-end;
        padding-right: 40px;
    }
}
</style>