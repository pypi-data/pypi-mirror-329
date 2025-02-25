<script setup>
import { ref, computed } from 'vue'


const emits = defineEmits(['change', 'update:modelValue'])

const props = defineProps({
    modelValue: {
        type: String,
        default: ''
    },
    editable: {
        type: Boolean,
        default: false
    },
    width: {
        default: 100
    },
    options: {
        type: Array,
        default: () => [],
    },
    type: {
        type: String,
        default: 'input'
    }
})

const tags = computed({
    get() {
        if (typeof props.modelValue == 'string') {
            if (props.modelValue.length !== 0) {
                return props.modelValue.split(',');
            }
        }
        return []
    },
    set(data) {
        emits('change', data.join(','))
        emits('update:modelValue', data.join(','))
    },
});

const valueMap = computed(() => {
    let tmp = {};
    props.options.forEach((option) => {
        tmp[option.value] = option.label;
    });
    return tmp;
})

const newTag = ref('')

const handlers = {
    add() {
        const temp = tags.value.slice()
        temp.push(newTag.value);
        tags.value = temp
        newTag.value = ''
    },
    remove(index) {
        tags.value.splice(index, 1)
        const temp = tags.value.slice()
        temp.splice(index, 1);
        tags.value = temp
    }
}
</script>


<template>
    <div class="xl-tags">
        <el-tag v-for="(tag, index) in tags" :key="tag" :closable="editable" @close="handlers.remove(index)">
            {{ type == 'select' ? valueMap[tag] : tag }}
        </el-tag>
        <xl-input v-if="editable && type == 'input'" class="new-tag" v-model="newTag" />
        <xl-search-select v-if="editable && type == 'select'" class="new-tag" v-model="newTag" :width="width"
            :options="options" />
        <xl-button v-if="editable" class="add-btn" @click="handlers.add">+ 添加</xl-button>
    </div>
</template>


<style lang="less" scoped>
.el-tag {
    margin-left: 3px;
    margin-bottom: 2px;
}

.xl-input {
    width: auto !important
}

.new-tag {
    margin-left: 3px;
    margin-bottom: 2px;
    height: 32px;
    line-height: 30px;
    padding-top: 0;
    padding-bottom: 0;
}

.add-btn {
    margin-left: 3px;
}
</style>