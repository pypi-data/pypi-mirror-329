<script setup>
import { ref, computed } from 'vue'


const emits = defineEmits(['confirm', 'finish'])

const props = defineProps({
    title: {},
    width: {},
    data: {},
    ruleMap: {
        default() {
            return {}
        }
    },
    labelWidth: {
        default: 70
    },
    callback: {
        type: Function,
        default: () => { },
    }
})

const refs = {
    dialog: ref(null),
    form: ref(null),
}

function convertRuleMapToRules(ruleMap) {
    const rules = {};

    for (const key in ruleMap) {
        rules[key] = [{ required: true, message: `请输入${ruleMap[key]}`, trigger: "blur" }];
    }

    return rules;
}

const rules = computed(() => convertRuleMapToRules(props.ruleMap));

async function validate() {
    let flag = 0
    await refs.form.value.validate(function (valid) {
        flag = valid
    })
    return flag
}

defineExpose({
    show() {
        refs.dialog.value.show()
    }
})
</script>


<template>
    <xl-dialog class="xl-edit-dialog" :ref="refs.dialog" :title="title" :width="width" :validate="validate"
        :callback="callback" @finish="emits('finish')">
        <el-form :ref="refs.form" :model="data" :rules="rules" :label-width="`${labelWidth}px`">
            <slot />
        </el-form>
    </xl-dialog>
</template>


<style lang="less">
.xl-edit-dialog {
    .xl-form-item {
        width: 100% !important;
    }
}
</style>