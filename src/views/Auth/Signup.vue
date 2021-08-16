<template>
  <div>
    <v-container class="pa-0">
      <v-row align="center" justify="space-between">
        <v-col>
          <div class="mb-4">
            <span class="text-h6 text--secondary">
              {{ $vuetify.lang.t("$vuetify.auth.sign-up.title") }}
            </span>
          </div>
          <h1 class="text-h5 mb-6">
            {{ $vuetify.lang.t("$vuetify.auth.sign-up.create") }}
          </h1>
          <v-form>
            <v-container class="pa-0">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    ref="input"
                    class="mb-2"
                    :label="$vuetify.lang.t('$vuetify.auth.sign-up.firstname')"
                    name="login"
                    type="text"
                    hide-details="auto"
                    outlined
                    :error-messages="error"
                    dense
                    v-model="first_name"
                  />
                </v-col>
                <v-col cols="12" md="6">
                  <v-text-field
                    ref="input"
                    class="mb-2"
                    :label="$vuetify.lang.t('$vuetify.auth.sign-up.lastname')"
                    name="login"
                    type="text"
                    hide-details="auto"
                    outlined
                    :error-messages="error"
                    dense
                    v-model="last_name"
                  />
                </v-col>
              </v-row>
              <v-text-field
                ref="input"
                class="mb-2"
                label="Username"
                name="login"
                type="text"
                hide-details="auto"
                persistent-hint
                outlined
                :error-messages="error"
                dense
                v-model="username"
              />
              <v-text-field
                ref="input"
                class="mb-2"
                :label="$vuetify.lang.t('$vuetify.auth.sign-up.email')"
                name="login"
                type="text"
                hide-details="auto"
                persistent-hint
                outlined
                :error-messages="error"
                dense
                v-model="email"
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
              <div class="body-2">
                {{ $vuetify.lang.t("$vuetify.auth.sign-up.password-props") }}
              </div>
            </v-container>
          </v-form>
          <div class="transition-wrapper">
            <div class="d-flex justify-space-between mt-8">
              <v-btn
                class="text-none letter-spacing-0"
                style="margin-left: -16px"
                color="primary"
                text
                @click="$router.push({ name: 'signin' })"
              >
                {{ $vuetify.lang.t("$vuetify.auth.sign-up.instead") }}
              </v-btn>
              <v-btn
                class="text-none letter-spacing-0"
                style="min-width: 88px"
                color="primary"
                depressed
                @click="signup"
              >
                {{ $vuetify.lang.t("$vuetify.auth.sign-up.next") }}
              </v-btn>
            </div>
            <!-- <transition :name="transitionName">
              <router-view @next="$emit('next', $event)" />
            </transition> -->
          </div>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { wip } from "@/helpers.js";

export default {
  data: () => ({
    transitionName: "",
    error: "",
    first_name: "",
    last_name: "",
    password: "",
    email: "",
    username: "",
  }),

  methods: {
    wip,
    signup() {
      this.$store
        .dispatch("userSignup", {
          username: this.username,
          password: this.password,
          email: this.email,
          first_name: this.first_name,
          last_name: this.last_name,
        })
        .then(() => {
          this.$router.push({ name: "signin" });
          this.$root.$emit(
            "showAlert",
            "Sign up successful. Please login!",
            "success"
          );
        })
        .catch((err) => {
          // console.log(err);
          this.$root.$emit(
            "showAlert",
            "Sign up unsuccessful. Please try again.",
            "success"
          );

          this.incorrectAuth = true;
        });
    },
  },
};
</script>
