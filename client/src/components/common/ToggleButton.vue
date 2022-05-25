<template>
  <div class="toggle-button">
    <div class="label">Hide disabled?</div>
    <div class="toggle-off" @click="toggle" v-if="isToggle === false">
      <font-awesome-icon icon="fa-solid fa-toggle-off" />
    </div>
    <div class="toggle-on" @click="toggle" v-else>
      <font-awesome-icon icon="fa-solid fa-toggle-on" />
    </div>
  </div>
</template>
<script>
import { eventBus } from "@/main";
export default {
  props: ["emitVar"],
  data() {
    return {
      isToggle: false,
    };
  },
  created() {},
  methods: {
    initEmitVar() {
      return this.emitVar;
    },
    toggle() {
      if (this.isToggle == false) {
        this.isToggle = true;
      } else {
        this.isToggle = false;
      }
      console.log("emit toggle " + this.initEmitVar() + " " + this.isToggle);
      eventBus.$emit(this.initEmitVar(), this.isToggle);
    },
  },
};
</script>
<style lang="scss" scoped>
.toggle-button {
  font-size: large;
  display: flex;
  justify-content: space-around;
  align-items: center;
  border-radius: $miniRadius;
  border: 0;
  font-size: large;
  cursor: pointer;

  .label {
    font-size: small;
  }

  .toggle-off {
    font-size: x-large;
  }

  .toggle-on {
    color: $tick;
    font-size: x-large;
  }
}
</style>
