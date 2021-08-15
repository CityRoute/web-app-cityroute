import Favourite from "@/components/Favourite.vue";
import { shallowMount, createLocalVue } from "@vue/test-utils";
import Vuex from "vuex";
import Vuetify from "vuetify";

const localVue = createLocalVue();
localVue.use(Vuex);
localVue.use(Vuetify);

var expect = require("expect");

describe("Favourite.vue", () => {
  let actions;
  let store;
  let state;
  let wrapper;
  beforeEach(() => {
    state = {
      accessToken: "",
    };
    actions = {};
    store = new Vuex.Store({
      actions,
      state,
    });
    wrapper = shallowMount(Favourite, {
      store,
      localVue,
      methods: {
        deleteFavourite: () => {},
        getFavouriteStops: () => {},
        getFavouriteRoutes: () => {},
        getFavouriteDirections: () => {},
      },
    });
  });

  it("Renders the component", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("Does header exist", () => {
    expect(wrapper.find("header")).toEqual({ selector: "header" });
  });
});
