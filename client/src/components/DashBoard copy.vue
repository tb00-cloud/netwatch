<template>
  <div class="dashboard-page">
    <div class="top">
      <div class="left"><SearchBar ref="searchBar" /></div>
      <div @click="showModal" class="right"><AddButton /></div>
    </div>
    <div class="bottom">
      <DashTable />
    </div>
    <PutTargetModal v-show="isModalVisible" @close="closeModal" />
  </div>
</template>

<script>
import SearchBar from "@/components/common/SearchBar.vue";
import AddButton from "@/components/common/AddButton.vue";
import DashTable from "@/components/common/DashTable.vue";
import PutTargetModal from "@/components/PutTargetModal.vue";
import { checkSessionState } from "@/services/check-session.service";
import { showToast } from "@/services/toast.service.js";
import { eventBus } from "@/main";
export default {
  data() {
    return {
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
  created() {
    checkSessionState();
  },
  destroyed() {
    eventBus.$off("dashSearchText");
  },
  components: {
    AddButton,
    SearchBar,
    DashTable,
    PutTargetModal,
  },
  methods: {
    showModal() {
      this.isModalVisible = true;
    },
    closeModal() {
      this.isModalVisible = false;
    },
    toasty(msg) {
      console.log("on toasty " + msg);
      showToast(msg, "info");
    },
    goTarget(id) {
      this.$router.push({ name: "target", query: { id } });
    },
  },
};
</script>
<style lang="scss" scoped>
.dashboard-page {
  display: flex;
  align-items: center;
  flex-direction: column;
  padding-top: 5%;
  width: 100%;
  height: 100%;

  .top {
    display: flex;
    width: 80%;
    justify-content: space-between;
    height: 3.5rem;
    background: $accent;
    border-radius: 0.5rem;

    .left {
      width: 95%;
    }

    .right {
      width: 5%;
    }
  }

  .bottom {
    margin: 1rem;
    display: flex;
    width: 80%;
    min-height: 90%;
  }
}
</style>
