<template>
  <!-- <div class="header"> -->
  <div class="navbar">
    <div class="left">
      <img class="logo" :src="images.logoWhite" />
      <div class="brand" @click="home">Net Watch</div>
      <div class="items">
        <div
          class="item"
          :class="{ active: this.$route.name === 'home' }"
          v-if="isLoggedIn"
          @click="home"
        >
          Dashboard
        </div>
        <div
          class="item"
          :class="{ active: this.$route.name === 'users' }"
          v-if="isLoggedIn"
          @click="users"
        >
          Users
        </div>
      </div>
    </div>
    <div class="right">
      <div class="welcome" v-if="isLoggedIn && username">
        Welcome, {{ username }}
      </div>
      <div class="logout" v-if="isLoggedIn" @click="onLogout">
        <font-awesome-icon icon="fa-solid fa-right-from-bracket" />
      </div>
    </div>
  </div>
</template>
<script>
import logoWhite from "@/assets/images/logo-white.svg";
import { checkSessionState } from "@/services/check-session.service";
import { showToast } from "@/services/toast.service";
import { eventBus } from "@/main";
export default {
  data() {
    return {
      images: {
        logoWhite,
      },
      isLoggedIn: false,
      username: null,
      path: "home",
    };
  },
  created() {
    this.setIsLoggedIn();
    eventBus.$on("loggedIn", () => {
      this.setIsLoggedIn();
    });
  },
  destroyed() {
    eventBus.$off("loggedIn");
  },
  watch: {
    $route(to) {
      this.path = to.name;
    },
  },

  methods: {
    setUser(user) {
      this.username = user;
    },
    setIsLoggedIn() {
      this.setUser(this.$session.get("username"));
      this.isLoggedIn = checkSessionState();
    },
    home() {
      this.$router.push({ name: "home" });
    },
    users() {
      this.$router.push({ name: "users" });
    },
    async onLogout() {
      try {
        const config = {
          headers: { "Content-Type": "application/json" },
          withCredentials: true,
        };
        this.axios.defaults.withCredentials = true;
        const res = await this.axios.post(
          "http://localhost:5000/logout",
          config
        );
        if (res.status == 200) {
          this.$session.destroy();
          this.setIsLoggedIn();
          this.$router.push({ name: "login" });
        }
      } catch (error) {
        showToast("Server error", "error");
      }
    },
  },
};
</script>
<style lang="scss" scoped>
// .header {
.navbar {
  display: flex;
  justify-content: space-between;
  background: $theme;
  height: 10%;
  // padding-bottom: 4rem;

  .left {
    display: flex;
    list-style: none;

    align-items: center;
    color: $white;
    padding-left: 1rem;
    cursor: pointer;

    .logo {
      display: flex;
      z-index: 999;
      padding: 1rem 1rem 0 0;
      height: 5rem;
      width: 5rem;
    }

    .brand {
      font-weight: bold;
      font-size: 2rem;
      padding-right: 3rem;
    }

    .items {
      display: flex;

      .item {
        font-size: large;
        margin-right: 1rem;
        cursor: pointer;
        padding: 0.2rem 0;
      }
    }

    .active {
      border-bottom: 2px solid $offWhite;
      // border-radius: 2px;
    }
  }

  .right {
    display: flex;
    align-items: center;
    padding-right: 3rem;
    color: $white;
    font-size: large;

    .welcome {
      display: flex;
      padding-right: 2.5rem;
    }

    .logout {
      display: flex;
      padding-right: 1rem;
      cursor: pointer;
    }
  }
}
// }
</style>
