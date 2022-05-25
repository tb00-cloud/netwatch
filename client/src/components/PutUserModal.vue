<template>
  <div class="modal-backdrop">
    <div class="modal">
      <header class="modal-header">
        <slot name="header">
          <p v-if="id">
            Edit User ID {{ id }}
            <font-awesome-icon icon="fa-solid fa-pen" />
          </p>
          <p v-else>New User</p>
        </slot>
      </header>
      <section class="modal-body">
        <label class="label" for="name">Username</label>
        <div class="label err">
          <li v-for="(error, id) in this.errors['username']" :key="id">
            {{ error }}
          </li>
        </div>
        <input
          type="text"
          class="input"
          name="username"
          maxlength="255"
          v-model="username"
          @keyup.enter="putUser"
        />
        <label v-if="id" class="label" for="enabled">Reset password?</label>
        <div v-if="id" class="input invisible">
          <input
            type="checkbox"
            value="false"
            class="radio"
            name="resetPassword"
            v-model="resetPassword"
          />
        </div>
        <label v-if="(id && resetPassword) || !id" class="label" for="password"
          >Password</label
        >
        <div class="label err">
          <li v-for="(error, id) in this.errors['password']" :key="id">
            {{ error }}
          </li>
        </div>
        <input
          v-if="(id && resetPassword) || !id"
          type="password"
          class="input"
          name="password"
          maxlength="255"
          v-model="password"
          @keyup.enter="putUser"
        />
        <label class="label" for="enabled">Enabled</label>
        <div class="input invisible">
          <input
            type="checkbox"
            value="true"
            class="radio"
            name="enabled"
            v-model="enabled"
          />
        </div>
      </section>
      <footer class="modal-footer">
        <button type="button" class="button close" @click="close">Close</button>
        <button type="button" class="button save" @click="putUser">Save</button>
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
      username: null,
      password: null,
      resetPassword: false,
      enabled: true,
      haveErrors: false,
      errors: {
        username: [],
        password: [],
      },
    };
  },
  name: "PutUserModal",
  created() {},
  watch: {
    eId: async function (newval) {
      this.id = newval;
      this.prePopulate(newval);
    },
  },
  methods: {
    async prePopulate(id) {
      console.log("prepopulatecalled");
      const data = await this.getData(id);
      this.username = data.username;
      this.enabled = data.enabled;
      console.log(this.username);
    },
    async getData(id) {
      console.log("getting data for: " + id);
      try {
        const res = await http({ user_ids: id }).get("users");
        if (res.status == 200) {
          console.log("the username is: " + res.data[0].username);
          return {
            username: res.data[0].username,
            enabled: res.data[0].enabled,
          };
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
    async putUser() {
      this.validate();
      if (this.haveErrors) {
        return;
      }
      var payload = {};
      if (this.id) {
        if (this.resetPassword) {
          payload = {
            id: this.id,
            username: this.username,
            new_password: btoa(this.password),
            enabled: this.enabled,
          };
        } else {
          payload = {
            id: this.id,
            username: this.username,
            enabled: this.enabled,
          };
        }
      } else {
        payload = {
          id: this.id,
          username: this.username,
          password: btoa(this.password),
          enabled: this.enabled,
        };
      }
      try {
        console.log(payload);
        const res = await http().put("users", payload);
        if (res.status == 200) {
          showToast("User saved", "success", 1500);
          eventBus.$emit("userAdded");
          this.clear();
          this.close();
        }
      } catch (error) {
        if (
          error.response &&
          error.response.status == 400 &&
          error.response.data.error == "this username is already taken"
        ) {
          var array = [];
          array.push("The username has already been taken");
          this.errors["username"] = array;
        } else if (error.response && error.response.status == 401) {
          showToast("Forbidden. Log in with a valid account", "error");
        } else {
          console.log(error);
          showToast("A server error ocurred", "error");
        }
      }
    },
    clear() {
      if (!this.eId) {
        this.resetPassword = false;
        this.username = null;
        this.password = null;
        this.enabled = true;
      }
    },
    validateUsername() {
      var array = [];

      if (this.username == null || this.username == "") {
        array.push("Required");
      } else if (!this.username.match(/^[A-Za-z0-9 _-]*$/)) {
        array.push(
          "Can only contain numbers, letters, spaces, underscores and hiphens"
        );
      }

      if (array.length > 0) {
        this.haveErrors = true;
      }
      this.errors["username"] = array;
    },
    validatePassword() {
      var array = [];

      let regex = new RegExp(
        /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,128}$/
      );

      if (this.id && this.resetPassword) {
        if (this.password == null || this.password == "") {
          array.push("Required");
        }

        if (!regex.test(this.password)) {
          array.push(
            "Must contain: number, letter, character (length 6 - 128)"
          );
        }
      } else {
        if (!regex.test(this.password)) {
          array.push(
            "Must contain: number, letter, character (length 6 - 128)"
          );
        }
      }

      if (array.length > 0) {
        this.haveErrors = true;
      }
      this.errors["password"] = array;
    },

    validate() {
      this.haveErrors = false;
      this.validateUsername();
      this.validatePassword();
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
</style>
