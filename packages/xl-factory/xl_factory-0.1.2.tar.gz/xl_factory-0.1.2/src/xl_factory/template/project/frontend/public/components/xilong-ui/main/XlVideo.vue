<template>
    <div class="plyr-wrapper">
      <video
        ref="videoPlayer"
        :src="src"
        :poster="poster"
        :crossorigin="crossorigin"
      >
        <source :src="src" :type="type" />
      </video>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue'
  import Plyr from 'plyr'
  import 'plyr/dist/plyr.css'
  
  const props = defineProps({
    src: {
      type: String,
      required: true
    },
    poster: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: 'video/mp4'
    },
    options: {
      type: Object,
      default: () => ({})
    },
    crossorigin: {
      type: String,
      default: 'anonymous'
    }
  })
  
  const videoPlayer = ref(null)
  let player = null
  
  onMounted(() => {
    // 初始化 Plyr
    player = new Plyr(videoPlayer.value, {
      controls: [
        'play-large',
        'play',
        'progress',
        'current-time',
        'mute',
        'volume',
        'captions',
        'settings',
        'pip',
        'airplay',
        'fullscreen'
      ],
      ...props.options
    })
  })
  
  onBeforeUnmount(() => {
    if (player) {
      player.destroy()
    }
  })
  
  // 可以暴露播放器实例，以便父组件控制
  defineExpose({
    player: () => player
  })
  </script>
  
  <style scoped>
  .plyr-wrapper {
    width: 100%;
    max-width: 100%;
  }
  </style>