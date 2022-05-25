<template>
  <div class="users-page">
    <div class="header">
      <div class="title">Manage Users</div>
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
      <UsersTable
        :hideDisabledToggleEvent="toggleEmitVar"
        :filterTextEvent="searchEmitVar"
      />
    </div>
    <PutUserModal v-show="isModalVisible" @close="closeModal" />
  </div>
</template>

<script>
import ToggleButton from "@/components/common/ToggleButton.vue";
import PutUserModal from "@/components/PutUserModal.vue";
import SearchBar from "@/components/common/SearchBar.vue";
import AddButton from "@/components/common/AddButton.vue";
import UsersTable from "@/components/common/UsersTable.vue";
import { checkSessionState } from "@/services/check-session.service";
export default {
  data() {
    return {
      toggleEmitVar: "hideDisabledUsers",
      searchEmitVar: "usersSearchText",
      isModalVisible: false,
    };
  },
  created() {
    checkSessionState();
  },
  components: {
    AddButton,
    SearchBar,
    UsersTable,
    ToggleButton,
    PutUserModal,
  },
  methods: {
    showModal() {
      this.isModalVisible = true;
    },
    closeModal() {
      this.isModalVisible = false;
    },
  },
};
</script>

<style lang="scss" scoped>
.users-page {
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
