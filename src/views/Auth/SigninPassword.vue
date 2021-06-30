<template>
  <div>
    <div class="text-center w-100">
      <h1 class="text-h5 mb-2">
        {{ $vuetify.lang.t("$vuetify.auth.sign-in-password.title") }}
      </h1>
      <v-chip
        class="mb-10"
        outlined
        link
        @click="$router.push({ name: 'signin' })"
      >
        <v-avatar left>
          <v-icon color="secondary"> mdi-account-circle </v-icon>
        </v-avatar>
        {{ this.$store.state.identifier }}
        <v-avatar right>
          <v-icon color="secondary"> mdi-chevron-down </v-icon>
        </v-avatar>
      </v-chip>

      <v-form v-on:submit.prevent="login">
        <v-text-field
          class="mb-10"
          v-model="password"
          :append-icon="show ? 'mdi-eye-off-outline' : 'mdi-eye-outline'"
          :label="
            $vuetify.lang.t('$vuetify.auth.sign-in-password.enter-password')
          "
          name="password"
          :type="show ? 'input' : 'password'"
          hide-details="auto"
          outlined
          @click:append="show = !show"
        />
      </v-form>

      <div class="d-flex justify-space-between">
        <v-btn
          class="text-none letter-spacing-0 font-weight-bold"
          style="margin-left: -16px"
          color="primary"
          text
          @click="wip"
        >
          {{
            $vuetify.lang.t("$vuetify.auth.sign-in-password.forgot-password")
          }}
        </v-btn>
        <v-btn
          class="text-none"
          style="min-width: 88px"
          color="primary"
          depressed
          @click="login"
        >
          {{ $vuetify.lang.t("$vuetify.auth.sign-in-password.next") }}
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script>
import { wip } from "@/helpers.js";

export default {
  data: () => ({
    show: false,
    username: "",
    incorrectAuth: false,
    password: "",
  }),

  computed: {},

  methods: {
    wip,
    login() {
      console.log(this.$store.state.identifier, this.$store.state.password);
      this.$store
        .dispatch("userLogin", {
          username: this.$store.state.identifier,
          password: this.password,
        })
        .then(() => {
          this.$router.push({ name: "MyAccount" });
        })
        .catch((err) => {
          console.log(err);
          this.incorrectAuth = true;
        });
    },
  },
};
</script>
