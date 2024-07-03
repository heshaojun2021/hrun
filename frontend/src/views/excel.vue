<template>
  <div>
    <a ref="externalLink" href="https://docs.qq.com/sheet/DY2VDZFd5d1B6c2Fr?tab=BB08J2" target="_blank"></a>
  </div>
</template>

<script>
export default {
  mounted() {
    // 获取 <a> 标签的引用
    const link = this.$refs.externalLink;

    // 打开链接
    if (link) {
      link.click(); // 模拟点击事件打开链接
    }
  }
};
</script>

<style>
</style>