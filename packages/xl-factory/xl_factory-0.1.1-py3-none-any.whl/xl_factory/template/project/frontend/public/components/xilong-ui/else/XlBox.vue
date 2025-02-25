<script setup>
const props = defineProps({
  text: {
    type: String,
    default: "",
  },
  height: {
    default: 300,
  }
});
</script>


<template>
  <div class="xl-box">
    <div class="header">
      <div class="left">
        <span class="title">{{ text }}</span>
      </div>
      <div class="right">
        <slot name="header-right" />
      </div>
    </div>
    <div class="main" :style="`height: ${height}px`">
      <slot />
    </div>
  </div>
</template>


<style lang="less">
.xl-box {
  background: #fff;
  color: #000;
  box-shadow: 2px 3px 4px #00000029;
  border-radius: 5px;
  border-top: 1px solid rgb(240, 240, 240);
  border-left: 1px solid rgb(240, 240, 240);
  padding: 10px 15px;
  margin: 5px;
  display: flex;
  flex-flow: column;

  .header {
    display: flex;
    padding-bottom: 10px;
    height: 40px;

    .left {
      flex: 1;

      .title {
        color: #2c2c2c;
        font-size: 17px;
        padding-bottom: 10px;
        font-family: "BlinkMacSystemFont, Segoe UI, Roboto, Oxygen, Cantarell, Fira Sans, Droid Sans, Helvetica Neue, sans-serif";
      }
    }

    .right {
      flex: 1;
      text-align: right;
    }
  }

  .number {
    font-size: 30px;
    text-align: center;
  }

  .main {
    width: 100%;
  }
}
</style>