<script setup>
import { ref } from 'vue'


const props = defineProps({
    url: {
        type: String,
        default: ''
    }
})

const visible = ref(false)


defineExpose({
    show() {
        visible.value = true
    }
})
</script>


<template>
    <el-dialog class="xl-image-preview-dialog" v-model="visible" width="50%">
        <el-image :src="url"></el-image>
    </el-dialog>
</template>
  

  
<style lang="less"></style>
  
  
  
         
  
  
  