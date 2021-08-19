<template>
  <div>
    <div class="text-center w-100">
      <h1 class="text-h5 mb-2">
        Forgot Password
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
          v-model="token"
          label="Your token"
          name="text"
          hide-details="auto"
          outlined
        />
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              ref="input"
              class="mb-2"
              :label="$vuetify.lang.t('$vuetify.auth.sign-up.password')"
              name="login"
              type="password"
              hide-details="auto"
              outlined
              :error-messages="error"
              dense
              v-model="password"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              ref="input"
              class="mb-2"
              label="Confirm"
              name="login"
              type="password"
              hide-details="auto"
              outlined
              :error-messages="error"
              dense
            />
          </v-col>
        </v-row>
      </v-form>

      <div class="text-right">
        <v-btn aria-label="vuetify-button"
          class="text-none"
          style="min-width: 88px"
          color="primary"
          depressed
          @click="reset"
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
    incorrectAuth: false,
    token: "",
    password: "",
  }),

  computed: {},

  methods: {
    wip,
    reset() {
      this.$store
        .dispatch("userForgotPasswordReset", {
          token: this.token,
          password: this.password,
        })
        .then(() => {
          this.$router.push({ name: "MyAccount" });
        })
        .catch((err) => {
          // console.log(err);
          this.incorrectAuth = true;
        });
    },
  },
};
</script>
