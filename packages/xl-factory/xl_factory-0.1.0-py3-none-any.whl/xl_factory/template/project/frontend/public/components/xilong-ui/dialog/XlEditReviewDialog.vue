<script setup>
import { ref, computed } from 'vue'


const emits = defineEmits(['confirm', 'pass', 'reject'])

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
    passCallback: {
        type: Function,
        default: () => { },
    },
    rejectCallback: {
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
    <xl-review-dialog class="xl-edit-review-dialog" :ref="refs.dialog" :title="title" :width="width"
        :validate="validate" :pass-callback="passCallback" :reject-callback="rejectCallback" @pass="emits('pass')"
        @reject="emits('reject')">
        <el-form :ref="refs.form" :model="data" :rules="rules" :label-width="`${labelWidth}px`">
            <slot />
        </el-form>
    </xl-review-dialog>
</template>


<style lang="less">
.xl-edit-review-dialog {
    .xl-form-item {
        width: 100% !important;
    }
}
</style>