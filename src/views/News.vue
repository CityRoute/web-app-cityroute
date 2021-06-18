<template>
  <div>
    <v-card>
      <v-tabs v-model="tab" align-with-title>
        <v-tabs-slider color="yellow"></v-tabs-slider>

        <v-tab v-for="item in items" :key="item">
          {{ item }}
        </v-tab>
      </v-tabs>
    </v-card>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-card flat>
          <a
            class="twitter-timeline"
            href="https://twitter.com/dublinbusnews?ref_src=twsrc%5Etfw"
            >Tweets by dublinbusnews</a
          >
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <VueRssFeed :feedUrl="feedUrl" :name="name" :limit="limit" />
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import VueRssFeed from "vue-rss-feed";

export default {
  name: "News",
  components: {
    VueRssFeed,
  },

  mounted() {
    let externalScript = document.createElement("script");
    externalScript.setAttribute(
      "src",
      "https://platform.twitter.com/widgets.js"
    );
    document.head.appendChild(externalScript);
  },
  data: () => ({
    model: null,
    tab: null,
    feedUrl: "https://www.dublinbus.ie/RSS/Rss-news/",
    name: "",
    limit: 5,
    items: ["Twitter", "RSS"],
    text:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
  }),
};
</script>
<style></style>
