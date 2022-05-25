<template>
  <div id="app">
    <NavBar />
    <div class="body">
      <div class="left">
        <div class="top"></div>
      </div>
      <div class="center">
        <div class="container"><router-view></router-view></div>
      </div>
      <div class="right">
        <div class="top"></div>
      </div>
    </div>
    <div class="version">Beta</div>
  </div>
</template>

<script>
import NavBar from "@/components/common/NavBar.vue";
import { checkSessionState } from "@/services/check-session.service";
export default {
  components: {
    NavBar,
  },
  created() {
    this.checkSess();
    this.checkSessInterval();
  },
  methods: {
    checkSess() {
      if (!checkSessionState() && this.$route.name !== "login") {
        this.$router.push({ name: "login" });
      }
    },
    checkSessInterval() {
      setInterval(() => {
        this.checkSess();
      }, 3000);
    },
  },
};
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Lato:wght@200;300;400;500&display=swap");
html,
body {
  padding: 0;
  margin: 0;
}
#app {
  font-family: Lato, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: $primaryFont;
  font-weight: 400;
  width: 100%;
  height: 100vh;
  background: $background;

  .body {
    display: flex;
    height: 90%;

    .left,
    .right {
      height: 100%;
      width: 10%;
    }

    .top {
      height: 8%;
      background: $theme;
    }

    .center {
      width: 90%;
      height: 100%;
      background: $theme;
      display: flex;

      .container {
        width: 100%;
        height: 100%;
        background: $white;
        box-shadow: 0px 0px 13px -4px #292929b5;
        border-top-left-radius: $radius;
        border-top-right-radius: $radius;
        z-index: 999;
        height: calc(100% - 1rem);
        margin-top: 1rem;
      }
    }

    .page {
      background: white;
    }
  }

  .version {
    color: $greyFont;
    font-size: small;
    position: fixed;
    bottom: 1rem;
    left: 1rem;
  }
}

.toast.bubble {
  font-family: Lato, sans-serif;
  // font-weight: bold;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.toast.toasted.bubble {
  .action {
    color: $primaryFont;
  }

  &.error {
    background: $error;
    font-weight: 600;
  }

  &.success {
    background: $success;
    font-weight: 600;
  }

  &.info {
    background: $info;
    font-weight: 600;
  }
}

.tooltip {
  display: block !important;
  z-index: 10000;
  font-family: Lato, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  max-width: 16rem;
  font-size: small;

  .tooltip-inner {
    background: $info;
    color: $white;
    border-radius: 16px;
    padding: 5px 10px 4px;
  }

  .tooltip-arrow {
    width: 0;
    height: 0;
    border-style: solid;
    position: absolute;
    margin: 5px;
    border-color: black;
    z-index: 1;
  }

  &[x-placement^="top"] {
    margin-bottom: 5px;

    .tooltip-arrow {
      border-width: 5px 5px 0 5px;
      border-left-color: transparent !important;
      border-right-color: transparent !important;
      border-bottom-color: transparent !important;
      bottom: -5px;
      left: calc(50% - 5px);
      margin-top: 0;
      margin-bottom: 0;
    }
  }

  &[x-placement^="bottom"] {
    margin-top: 5px;

    .tooltip-arrow {
      border-width: 0 5px 5px 5px;
      border-left-color: transparent !important;
      border-right-color: transparent !important;
      border-top-color: transparent !important;
      top: -5px;
      left: calc(50% - 5px);
      margin-top: 0;
      margin-bottom: 0;
    }
  }

  &[x-placement^="right"] {
    margin-left: 10px;

    .tooltip-arrow {
      border-width: 5px 5px 5px 0;
      border-left-color: transparent !important;
      border-top-color: transparent !important;
      border-bottom-color: transparent !important;
      left: -5px;
      top: calc(50% - 5px);
      margin-left: 0;
      margin-right: 0;
    }
  }

  &[x-placement^="left"] {
    margin-right: 5px;

    .tooltip-arrow {
      border-width: 5px 0 5px 5px;
      border-top-color: transparent !important;
      border-right-color: transparent !important;
      border-bottom-color: transparent !important;
      right: -5px;
      top: calc(50% - 5px);
      margin-left: 0;
      margin-right: 0;
    }
  }

  &.popover {
    $color: #f9f9f9;

    .popover-inner {
      background: $color;
      color: black;
      padding: 24px;
      border-radius: 5px;
      box-shadow: 0 5px 30px rgba(black, 0.1);
    }

    .popover-arrow {
      border-color: $color;
    }
  }

  &[aria-hidden="true"] {
    visibility: hidden;
    opacity: 0;
    transition: opacity 0.15s, visibility 0.15s;
  }

  &[aria-hidden="false"] {
    visibility: visible;
    opacity: 1;
    transition: opacity 0.15s;
  }
}
</style>
