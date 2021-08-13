import { shallowMount } from '@vue/test-utils'
import Favourite from "@/components/Favourite.vue";

describe('HelloWorld.vue', () => {
  it('renders props.msg when passed', () => {
    const msg = 'new message'
    const wrapper = shallowMount(Favourite, {
      propsData: { msg },
    });
    expect(wrapper.text()).toMatch(msg)
  })
})
