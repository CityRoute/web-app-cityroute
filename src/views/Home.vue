<template>
  <div>
    <BusMap />
  </div>
</template>

<script>
import BusMap from "../components/BusMap";

export default {
  name: "Home",

  components: {
    BusMap,
  },
};
</script>

<style>
html {
  scrollbar-width: none; /* For Firefox */
  -ms-overflow-style: none; /* For Internet Explorer and Edge */
}

html::-webkit-scrollbar {
  width: 0px; /* For Chrome, Safari, and Opera */
}
</style>
