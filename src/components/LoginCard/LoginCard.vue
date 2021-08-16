<template>
  <component :is="component" v-bind="$attrs">
    <slot />
  </component>
</template>

<script>
import LoginCardMobile from "./LoginCardMobile";

export default {
  computed: {
    component() {
      return LoginCardMobile;
    },
  },
};
</script>
