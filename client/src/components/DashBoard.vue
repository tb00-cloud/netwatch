<template>
  <div class="dashboard-page">
    <div class="header">
      <div class="title">Watch Targets</div>
      <div class="filter-container">
        <div class="toggle-disabled">
          <ToggleButton :emitVar="toggleEmitVar" />
        </div>
        <div class="search-bar">
          <SearchBar ref="searchBar" :emitVar="searchEmitVar" />
        </div>
        <div @click="showModal" class="add-button"><AddButton /></div>
      </div>
    </div>
    <div class="body">
      <DashTable
        :hideDisabledToggleEvent="toggleEmitVar"
        :filterTextEvent="searchEmitVar"
      />
    </div>

    <PutTargetModal v-show="isModalVisible" @close="closeModal" />
  </div>
</template>

<script>
import ToggleButton from "@/components/common/ToggleButton.vue";
import SearchBar from "@/components/common/SearchBar.vue";
import AddButton from "@/components/common/AddButton.vue";
import DashTable from "@/components/common/DashTable.vue";
import PutTargetModal from "@/components/PutTargetModal.vue";
import { eventBus } from "@/main";
export default {
  data() {
    return {
      toggleEmitVar: "hideDisalbedTargets", //The event name shared between toggle component and table component
      searchEmitVar: "dashSearchText",
      isModalVisible: false,
      tableData: null,
      showForm: true,
      newTarget: {
        name: null,
        host: null,
        port: null,
        enabled: true,
      },
      axiosConfig: {
        headers: { "Content-Type": "application/json" },
        withCredentials: true,
      },
    };
  },
  created() {},
  destroyed() {
    eventBus.$off("dashSearchText");
  },
  components: {
    AddButton,
    SearchBar,
    DashTable,
    PutTargetModal,
    ToggleButton,
  },
  methods: {
    count() {
      console.log("called");
      return "hello";
    },
    showModal() {
      this.isModalVisible = true;
    },
    closeModal() {
      this.isModalVisible = false;
    },
    goTarget(id) {
      this.$router.push({ name: "target", query: { id } });
    },
  },
};
</script>
<style lang="scss" scoped>
.dashboard-page {
  .header {
    display: flex;
    justify-content: space-between;

    .title {
      font-size: xx-large;
      font-weight: 400;
      font: $primaryFont;
      display: flex;
      padding: 2rem 0 0 4rem;
    }

    .filter-container {
      font-size: x-large;
      font-weight: 400;
      font: $primaryFont;
      display: flex;
      justify-content: flex-end;
      align-items: center;
      padding: 2rem 2.8rem 0 0;
      width: 50%;
    }

    .toggle-disabled {
      width: 10rem;
    }

    .search-bar {
      width: 20rem;
      margin-left: 0.2rem;
    }

    .add-button {
      width: 2rem;
      margin-left: 0.2rem;
    }
  }

  .body {
    padding: 3rem;
  }
}
</style>
