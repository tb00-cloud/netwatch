<template>
  <div class="login-page">
    <div class="login-form">
      <div class="h1">Login...</div>
      <div class="spacer"></div>
      <input
        @keyup.enter="onLogin"
        type="text"
        placeholder="Enter username"
        class="input"
        name="username"
        required
        v-model="username"
      />
      <div class="spacer"></div>
      <input
        @keyup.enter="onLogin"
        type="password"
        placeholder="Enter password"
        class="input"
        name="password"
        required
        v-model="password"
      />
      <div class="spacer"></div>
      <button class="button" @click="onLogin">Login</button>
      <div class="spacer"></div>
    </div>
  </div>
</template>

<script>
import { http } from "@/services/axios.service";
import { showToast } from "@/services/toast.service";
import { eventBus } from "@/main";
export default {
  data() {
    return {
      username: null,
      password: null,
    };
  },
  methods: {
    async onLogin() {
      try {
        const res = await http().post("login", {
          username: this.username,
          password: btoa(this.password),
        });
        if (res.status == 200) {
          this.$session.start();
          this.$session.set("username", this.username);
          eventBus.$emit("loggedIn", this.username);
          this.$router.push({ name: "home" });
        }
      } catch (error) {
        if (error.response && error.response.status == 401) {
          showToast("Invalid username or password", "error");
        } else {
          showToast("Server error", "error");
        }
      }
    },
  },
};
</script>
<style lang="scss" scoped>
.login-page {
  display: flex;
  justify-content: center;
  padding-top: 5%;
  width: 100%;
  // height: 100%;

  .login-form {
    width: 20%;
    min-width: 15rem;
    min-height: 12rem;
    height: 30%;
    display: flex;
    flex-direction: column;
    padding: 1rem;

    .h1 {
      font-weight: bold;
      font-size: xx-large;
      text-align: left;
      padding: 0 0 2rem 0.5rem;
      color: rgb(54, 54, 54);
    }

    .spacer {
      height: 1rem;
    }

    .input {
      height: 2.3rem;
      border-style: none;
      border-radius: $miniRadius;
      background-color: $offWhite;
      padding-left: 1rem;
      box-shadow: $elementShadow;
    }

    .button {
      height: 2.3rem;
      border-style: none;
      border-radius: $miniRadius;
      background-color: $highlight;
      color: $primaryFont;
      font-size: large;
      padding-left: 1rem;
      cursor: pointer;
      box-shadow: $elementShadow;
    }
  }
}
</style>
