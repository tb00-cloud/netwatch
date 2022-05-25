<template>
  <div class="modal-backdrop">
    <div class="modal">
      <header class="modal-header">
        <slot name="header">
          <p v-if="id">
            Edit Target ID {{ id }}
            <font-awesome-icon icon="fa-solid fa-pen" />
          </p>
          <p v-else>New Watch Target</p>
        </slot>
      </header>
      <section class="modal-body">
        <label class="label" for="name"
          >Name
          <span class="tooltip">
            <font-awesome-icon
              tabindex="-1"
              v-tooltip.right="'Target friendly name. Has not technical effect'"
              icon="fa-solid fa-circle-question"
            />
          </span>
        </label>
        <div class="label err">
          <li v-for="(error, id) in this.errors['name']" :key="id">
            {{ error }}
          </li>
        </div>
        <input
          type="text"
          class="input"
          name="name"
          maxlength="255"
          v-model="name"
          @keyup.enter="putTarget"
        />
        <label class="label" for="host"
          >Host
          <span class="tooltip">
            <font-awesome-icon
              tabindex="-1"
              v-tooltip.right="'Host domain or IP address'"
              icon="fa-solid fa-circle-question"
            />
          </span>
        </label>
        <div class="label err">
          <li v-for="(error, id) in this.errors['host']" :key="id">
            {{ error }}
          </li>
        </div>
        <input
          type="text"
          class="input"
          name="host"
          maxlength="255"
          v-model="host"
          @keyup.enter="putTarget"
        />
        <label class="label" for="port">port</label>
        <div class="label err">
          <li v-for="(error, id) in this.errors['port']" :key="id">
            {{ error }}
          </li>
        </div>
        <input
          type="number"
          class="input"
          name="port"
          v-model="port"
          oninput="javascript: if (this.value.length > 5) this.value = this.value.slice(0, 5);"
          @keyup.enter="putTarget"
        />
        <label class="label" for="interval"
          >Interval (seconds)
          <span class="tooltip">
            <font-awesome-icon
              tabindex="-1"
              v-tooltip.right="
                'Number of seconds to wait beteen probes. This is also the timeout'
              "
              icon="fa-solid fa-circle-question"
            />
          </span>
        </label>
        <div class="label err">
          <li v-for="(error, id) in this.errors['interval']" :key="id">
            {{ error }}
          </li>
        </div>
        <input
          type="number"
          class="input"
          name="interval"
          v-model="interval"
          oninput="javascript: if (this.value.length > 10) this.value = this.value.slice(0, 10);"
          @keyup.enter="putTarget"
        />
        <label class="label" for="retentionVal"
          >History Retention Period
          <span class="tooltip">
            <font-awesome-icon
              tabindex="-1"
              v-tooltip.right="
                'Combined with History Retention Unit, this forms the amount of time the system will retain history'
              "
              icon="fa-solid fa-circle-question"
            />
          </span>
        </label>
        <div class="label err">
          <li v-for="(error, id) in this.errors['retentionVal']" :key="id">
            {{ error }}
          </li>
        </div>
        <input
          type="number"
          class="input"
          name="retentionVal"
          v-model="retentionVal"
          oninput="javascript: if (this.value.length > 10) this.value = this.value.slice(0, 10);"
          @keyup.enter="putTarget"
        />
        <label class="label" for="retentionUnit"
          >History Retention Unit<span class="tooltip">
            <font-awesome-icon
              tabindex="-1"
              v-tooltip.right="
                'Combined with History Retention Period, this forms the amount of time the system will retain history. E.g. 7 DAY'
              "
              icon="fa-solid fa-circle-question"
            /> </span
        ></label>
        <select
          v-model="retentionUnit"
          name="retentionUnit"
          class="input"
          id="retentionUnit"
        >
          <option value="MINUTE">MINUTE</option>
          <option value="HOUR">HOUR</option>
          <option value="DAY">DAY</option>
          <option value="WEEK">WEEK</option>
          <option value="MONTH">MONTH</option>
          <option value="QUARTER">QUARTER</option>
          <option value="YEAR">YEAR</option>
        </select>
        <label class="label" for="enabled"
          >Enabled
          <span class="tooltip">
            <font-awesome-icon
              tabindex="-1"
              v-tooltip.right="
                'If disabled, this target will not be watched (no probes sent)'
              "
              icon="fa-solid fa-circle-question"
            />
          </span>
        </label>
        <div class="input invisible">
          <input
            type="checkbox"
            value="true"
            class="radio"
            name="enabled"
            v-model="enabled"
            @keyup.enter="putTarget"
          />
        </div>
      </section>
      <footer class="modal-footer">
        <button type="button" class="button close" @click="close">Close</button>
        <button type="button" class="button save" @click="putTarget">
          Save
        </button>
      </footer>
    </div>
  </div>
</template>

<script>
import { showToast } from "@/services/toast.service";
import { http } from "@/services/axios.service";
import { eventBus } from "@/main";
export default {
  props: ["eId"],
  data() {
    return {
      id: null,
      name: null,
      host: null,
      port: null,
      enabled: true,
      interval: 5,
      retentionVal: 7,
      retentionUnit: "DAY",
      haveErrors: false,
      errors: {
        name: [],
        host: [],
        port: [],
        interval: [],
        retentionVal: [],
      },
    };
  },
  name: "PutTargetModal",
  created() {},
  watch: {
    eId: async function (newval) {
      this.id = newval;
      this.getData(newval);
    },
  },
  methods: {
    async getData(id) {
      try {
        const res = await http({ target_ids: id }).get("targets");
        if (res.status == 200) {
          this.host = res.data[0].host;
          this.name = res.data[0].name;
          this.port = res.data[0].port;
          this.enabled = res.data[0].enabled;
          this.interval = res.data[0].interval;
          this.retentionVal = res.data[0].retentionVal;
          this.retentionUnit = res.data[0].retentionUnit;
        }
      } catch (error) {
        if (error.response && error.response.status == 401) {
          showToast("Forbidden. Log in with a valid account", "error");
        } else {
          showToast("A server error ocurred", "error");
        }
      }
    },
    close() {
      this.$emit("close");
    },
    async putTarget() {
      this.validate();
      console.log(this.haveErrors);
      if (this.haveErrors) {
        return;
      }
      try {
        const res = await http().put("targets", {
          id: this.id,
          name: this.name,
          host: this.host,
          port: this.port,
          enabled: this.enabled,
          interval: this.interval,
          retentionVal: this.retentionVal,
          retentionUnit: this.retentionUnit,
        });
        if (res.status == 200) {
          showToast("Target saved", "success", 1500);
          eventBus.$emit("targetAdded");
          this.clear();
          this.close();
        }
      } catch (error) {
        if (error.response && error.response.status == 401) {
          showToast("Forbidden. Log in with a valid account", "error");
        } else {
          console.log(error);
          showToast("A server error ocurred", "error");
        }
      }
    },
    clear() {
      if (!this.eId) {
        this.name = null;
        this.host = null;
        this.port = null;
        this.enabled = true;
        this.interval = 5;
        this.retentionVal = 7;
        this.retentionUnit = "DAY";
      }
    },
    validateName() {
      var array = [];

      if (this.name == null || this.name == "") {
        array.push("Required");
      } else if (!this.name.match(/^[A-Za-z0-9 _-]*$/)) {
        array.push(
          "Can only contain numbers, letters, spaces, underscores and hiphens"
        );
      }

      if (array.length > 0) {
        this.haveErrors = true;
      }
      this.errors["name"] = array;
    },
    validateHost() {
      var array = [];

      var domainRx = new RegExp(
        /^((?:(?:(?:\w[\.\-\+]?)*)\w)+)((?:(?:(?:\w[\.\-\+]?){0,62})\w)+)\.(\w{2,6})$/ // eslint-disable-line
      );
      var ipv4Rx = new RegExp(
        /^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$/gi // eslint-disable-line
      );
      var ipv6Rx = new RegExp(
        /^(?:(?:[a-fA-F\d]{1,4}:){7}(?:[a-fA-F\d]{1,4}|:)|(?:[a-fA-F\d]{1,4}:){6}(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}|:[a-fA-F\d]{1,4}|:)|(?:[a-fA-F\d]{1,4}:){5}(?::(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}|(?::[a-fA-F\d]{1,4}){1,2}|:)|(?:[a-fA-F\d]{1,4}:){4}(?:(?::[a-fA-F\d]{1,4}){0,1}:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}|(?::[a-fA-F\d]{1,4}){1,3}|:)|(?:[a-fA-F\d]{1,4}:){3}(?:(?::[a-fA-F\d]{1,4}){0,2}:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}|(?::[a-fA-F\d]{1,4}){1,4}|:)|(?:[a-fA-F\d]{1,4}:){2}(?:(?::[a-fA-F\d]{1,4}){0,3}:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}|(?::[a-fA-F\d]{1,4}){1,5}|:)|(?:[a-fA-F\d]{1,4}:){1}(?:(?::[a-fA-F\d]{1,4}){0,4}:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}|(?::[a-fA-F\d]{1,4}){1,6}|:)|(?::(?:(?::[a-fA-F\d]{1,4}){0,5}:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(?:\\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)){3}|(?::[a-fA-F\d]{1,4}){1,7}|:)))(?:%[0-9a-zA-Z]{1,})?$/gm // eslint-disable-line
      );

      if (this.host == null || this.host == "") {
        array.push("Required");
      } else if (
        !this.host.match(domainRx) &&
        !this.host.match(ipv4Rx) &&
        !this.host.match(ipv6Rx)
      ) {
        array.push("Not a valid domain or IP");
      }

      if (array.length > 0) {
        this.haveErrors = true;
      }
      this.errors["host"] = array;
    },
    validatePort() {
      var array = [];

      if (this.port == null || this.port == "") {
        array.push("Required");
      }

      if (array.length > 0) {
        this.haveErrors = true;
      }
      this.errors["port"] = array;
    },
    validateInterval() {
      var array = [];

      if (this.interval == null) {
        array.push("Required");
      } else if (this.interval < 2) {
        array.push("Must 2 or more");
      }

      if (array.length > 0) {
        this.haveErrors = true;
      }
      this.errors["interval"] = array;
    },
    validateRetention() {
      var array = [];

      if (this.retentionVal == null || this.retentionVal == "") {
        array.push("Required");
      }

      if (array.length > 0) {
        this.haveErrors = true;
      }
      this.errors["retentionVal"] = array;
    },
    validate() {
      this.haveErrors = false;
      this.validateName();
      this.validateHost();
      this.validatePort();
      this.validateInterval();
      this.validateRetention();
    },
  },
};
</script>

<style lang="scss" scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: #ffffff;
  box-shadow: 2px 2px 20px 1px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 0.2rem;
  width: 35%;
}

.modal-header,
.modal-footer {
  padding: 15px;
  display: flex;
}

.modal-header {
  position: relative;
  border-bottom: 1px solid #eeeeee;
  color: $primaryFont;
  justify-content: space-around;
  font-weight: bold;
  font-size: large;
}

.modal-footer {
  border-top: 1px solid #eeeeee;
  justify-content: space-around;
  width: 90%;
}

.modal-body {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 1rem;

  .label {
    width: 90%;
    text-align: left;
    display: flex;
    align-items: center;

    &.err {
      padding-top: 0.5rem;
      font-size: small;
      color: red;
    }
  }

  .input {
    height: 2rem;
    width: 90%;
    margin: 0.3rem 0 1rem;
    border-bottom: 1px solid $greyBorder;
    border-top: 0;
    border-left: 0;
    border-right: 0;
    color: rgb(102, 102, 102);
    padding-left: 1rem;

    &.invisible {
      display: flex;
      justify-content: left;
      align-items: center;
      border: 0;
    }
  }
}

.button {
  height: 2rem;
  color: $primaryFont;
  background: $highlight;
  border: 0;
  border-radius: 0.2rem;
  cursor: pointer;

  &.close {
    width: 38%;
  }

  &.save {
    width: 60%;
  }
}

.tooltip {
  font-size: small;
  padding-left: 0.5rem;
}
</style>
