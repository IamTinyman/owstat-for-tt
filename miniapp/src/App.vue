<script setup lang="ts">
import { onLaunch } from '@dcloudio/uni-app'

onLaunch(() => {
  const authed = uni.getStorageSync('overstats_auth')
  if (!authed) {
    uni.reLaunch({ url: '/pages/login/index' })
  }
})
</script>

<style lang="scss">
@use '@/uni.scss';
</style>
