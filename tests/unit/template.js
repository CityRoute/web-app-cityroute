import template_name from "@/components/template_name.vue";
import { shallowMount, createLocalVue } from "@vue/test-utils";
import Vuex from "vuex";
import Vuetify from "@/plugins/vuetify"; // path to vuetify export

const localVue = createLocalVue();
localVue.use(Vuex);
localVue.use(Vuetify);

var expect = require("expect");

describe("template_name.vue", () => {
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
    wrapper = shallowMount(template_name, {
      store,
      localVue,
      methods: {},
    });
  });

  it("Renders the component", () => {
    expect(wrapper.exists()).toBe(true);
  });
});
