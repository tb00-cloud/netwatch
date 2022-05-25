<template>
  <div class="searchbar-container">
    <input
      type="search"
      placeholder="Search..."
      class="search"
      name="search"
      v-model="searchText"
      @keyup.enter="search"
    />
    <div @click="search" class="button">
      <font-awesome-icon icon="fa-solid fa-magnifying-glass" />
    </div>
  </div>
</template>
<script>
import { eventBus } from "@/main";
export default {
  props: ["emitVar"],
  data() {
    return {
      searchText: "",
    };
  },
  methods: {
    initEmitVar() {
      return this.emitVar;
    },
    search() {
      eventBus.$emit(this.initEmitVar(), this.searchText);
    },
  },
};
</script>
<style lang="scss" scoped>
.searchbar-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;

  .search {
    background: $offWhite;
    width: 90%;
    height: 2rem;
    border: 0;
    border-radius: 0.2rem;
    padding: 1rem;
    box-shadow: $elementShadow;
  }

  .button {
    display: flex;
    justify-content: center;
    align-items: center;
    background: $highlight;
    width: 2rem;
    height: 2rem;
    border: 0;
    font-size: medium;
    border-radius: $miniRadius;
    cursor: pointer;
    margin-left: 0.4rem;
    box-shadow: $elementShadow;
  }
}
</style>
