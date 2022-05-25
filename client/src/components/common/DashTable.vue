<template>
  <div class="table">
    <ConfirmModal
      v-show="confirmModalVisible"
      @close="closeConfirmModal"
      @proceed="deleteTarget"
      :msg="confirmMessage"
    />
    <div class="header row">
      <div class="col col-1">ID</div>
      <div class="col col-2">Name</div>
      <div class="col col-3">Host</div>
      <div class="col col-4">Port</div>
      <div class="col col-5">Interval (sec)</div>
      <div class="col col-6">Enabled</div>
      <div class="col col-7"></div>
    </div>
    <div class="spacer"></div>
    <div v-for="row in data" :key="row.id" class="row">
      <div class="col col-1">{{ row.id }}</div>
      <div class="col col-2">{{ row.name }}</div>
      <div class="col col-3">{{ row.host }}</div>
      <div class="col col-4">{{ row.port }}</div>
      <div class="col col-5">{{ row.interval }}</div>
      <div class="col col-6">
        <span class="green" v-if="row.enabled === 1">
          <font-awesome-icon icon="fa-solid fa-check" />
        </span>
        <span :class="{ red: row.enabled !== 1 }" v-else>
          <font-awesome-icon icon="fa-solid fa-xmark" />
        </span>
      </div>
      <div class="col col-6">
        <font-awesome-icon
          @click="showConfirmModal(row.name, row.id)"
          class="action trash"
          icon="fa-solid fa-trash-can"
        />
        <font-awesome-icon
          @click="goTarget(row.id)"
          class="action"
          icon="fa-solid fa-chart-line"
        />
        <font-awesome-icon
          @click="showPutModal(row.id)"
          class="action edit"
          icon="fa-solid fa-pen"
        />
      </div>
    </div>
    <PutTargetModal
      :eId="putModalTargetID"
      v-show="isPutModalVisible"
      @close="closePutModal"
    />
  </div>
</template>

<script>
import PutTargetModal from "@/components/PutTargetModal.vue";
import ConfirmModal from "@/components/common/ConfirmModal.vue";
import { http } from "@/services/axios.service.js";
import { showToast } from "@/services/toast.service.js";
import { eventBus } from "@/main";
export default {
  props: ["hideDisabledToggleEvent", "filterTextEvent"],
  data() {
    return {
      data: null,
      allData: null,
      confirmModalVisible: false,
      confirmMessage: null,
      filterText: "",
      filterEnabled: false,
      deleteID: null,
      isPutModalVisible: false,
      putModalTargetID: null,
    };
  },
  components: {
    ConfirmModal,
    PutTargetModal,
  },
  created() {
    this.getData();
    eventBus.$on(this.initPropFilterTextEvent(), (payload) => {
      this.filterData(payload);
      this.filterText = payload;
    });
    eventBus.$on(this.initPropHideDisabledToggleEvent(), (payload) => {
      this.filterEnable(payload);
      this.filterData(this.filterText);
    });
    eventBus.$on("targetAdded", () => {
      this.getData();
    });
  },
  destroyed() {
    eventBus.$off(this.initPropHideDisabledToggleEvent());
    eventBus.$off(this.initPropFilterTextEvent());
    eventBus.$off("targetAdded");
  },
  methods: {
    initPropHideDisabledToggleEvent() {
      return this.hideDisabledToggleEvent;
    },
    initPropFilterTextEvent() {
      return this.filterTextEvent;
    },
    showPutModal(id) {
      this.putModalTargetID = id;
      this.isPutModalVisible = true;
    },
    closePutModal() {
      this.isPutModalVisible = false;
    },
    showConfirmModal(name, id) {
      this.deleteID = id;
      this.confirmMessage = "Delete " + name + "? ID:" + id;
      this.confirmModalVisible = true;
    },
    closeConfirmModal() {
      this.confirmModalVisible = false;
    },
    async getData() {
      try {
        const res = await http().get("targets");
        if (res.status == 200) {
          const mappedData = res.data.map((data) => {
            return {
              id: data.ID.toString(),
              host: data.host.toString(),
              name: data.name.toString(),
              port: data.port.toString(),
              interval: data.interval.toString(),
              enabled: data.enabled,
            };
          });
          this.data = mappedData;
          this.allData = mappedData;
        }
      } catch (error) {
        console.log(error);
        if (error.response && error.response.status == 401) {
          showToast("Forbidden. Log in with a valid account", "error");
        } else {
          showToast("Couldn't load target data", "error");
        }
      }
    },
    async deleteTarget() {
      try {
        const deleteID = this.deleteID;
        const res = await http({ target_ids: deleteID }).delete("targets");
        if (res.status == 200) {
          showToast("Target deleted", "success");
          await this.getData();
          if (this.filterText) {
            this.filterData(this.filterText);
          }
        }
      } catch (error) {
        if (error.response && error.response.status == 401) {
          showToast("Forbidden. Log in with a valid account", "error");
        } else {
          showToast("A server error ocurred", "error");
        }
      }
      this.closeConfirmModal();
    },
    filterData(text) {
      text = text.toLowerCase();
      this.data = this.allData.filter((data) => {
        if (this.filterEnabled == true && data.enabled !== 1) {
          return false;
        }
        return (
          data.id.includes(text) ||
          data.host.includes(text) ||
          data.name.includes(text) ||
          data.port.includes(text) ||
          data.interval.includes(text)
        );
      });
    },
    filterEnable(enabled) {
      if (enabled == 1) {
        this.filterEnabled = 1;
      } else {
        this.filterEnabled = 0;
      }
    },
    goTarget(id) {
      this.$router.push({
        name: "target",
        params: { id },
      });
    },
  },
};
</script>

<style lang="scss" scoped>
.table {
  width: 100%;
  display: flex;
  flex-direction: column;

  .spacer {
    width: 100%;
    height: 1rem;
  }

  .row {
    display: flex;
    width: 100%;
    height: 2.5rem;

    .col {
      display: flex;
      justify-content: center;
      align-items: center;
      width: 10%;

      .green {
        color: $tick;
      }

      .red {
        color: $cross;
      }

      &.red {
        color: $cross;
      }

      &.col-2 {
        width: 25%;
      }

      &.col-3 {
        width: 25%;
      }

      &.col-6 {
        width: 10%;
        display: flex;
        justify-content: space-around;

        .action {
          cursor: pointer;

          &.trash {
            color: $delete;
          }

          &.edit {
            color: $highlight;
          }

          &:not(:hover) {
            color: $greyFont;
          }
        }
      }
    }

    &.header {
      height: 3rem;
      border-bottom: solid 2px $underline;
      color: $primaryFont;
      font-weight: bold;
      padding-bottom: 1rem;
    }
  }
}
</style>
