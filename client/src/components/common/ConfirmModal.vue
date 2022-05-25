<template>
  <div class="modal-backdrop">
    <div class="modal">
      <header class="modal-header">
        <slot name="header">Are you sure?</slot>
      </header>
      <section class="modal-body">
        <div class="content">{{ msg }}</div>
      </section>
      <footer class="modal-footer">
        <button type="button" class="button close" @click="close">Canel</button>
        <button type="button" class="button save" @click="proceed">
          Proceed
        </button>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  props: ["msg"],
  name: "ConfirmModal",
  methods: {
    close() {
      this.$emit("close");
    },
    proceed() {
      this.$emit("proceed");
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
  width: 25%;
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
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 1rem;
}

.button {
  height: 2rem;
  color: $primaryFont;
  background: $highlight;
  border: 0px solid $theme;
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
