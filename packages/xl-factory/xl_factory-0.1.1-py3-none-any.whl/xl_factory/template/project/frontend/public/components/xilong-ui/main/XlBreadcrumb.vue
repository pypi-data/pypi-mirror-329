<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const breadcrumbData = ref([]);

const bread = () => {
    let matched = route.matched.filter(item => item.name);
    breadcrumbData.value = matched;
};

watch(route, bread);

onMounted(bread);
</script>


<template>
    <el-breadcrumb class="xl-breadcrumb" separator="/">
        <el-breadcrumb-item v-for="(item, index) in breadcrumbData" :key="index" :to="item.path">
            {{ item.name }}
        </el-breadcrumb-item>
    </el-breadcrumb>
</template>
  

  
<style scoped></style>