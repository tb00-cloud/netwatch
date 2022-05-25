<template>
  <div class="add-button">
    <font-awesome-icon icon="fa-solid fa-plus" />
  </div>
</template>
<script>
export default {
  data() {
    return {};
  },
  created() {},
  methods: {},
};
</script>
<style lang="scss" scoped>
.add-button {
  width: 2rem;
  height: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  background: $highlight;
  border-radius: $miniRadius;
  border: 0;
  font-size: large;
  cursor: pointer;
  box-shadow: $elementShadow;
}
</style>
