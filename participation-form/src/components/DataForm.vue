<template>
  <VeeForm class="flex gap-5 py-10 text-xs" @submit="submitForm">
    <section class="flex flex-col gap-2" id="first-name">
      <Field
        class="w-52 px-2 py-3"
        type="text"
        name="first-name"
        placeholder="First name"
        v-model="form.first_name"
        :rules="validateName"
        :disabled="!isAuthenticated"
      />
      <ErrorMessage class="text-red-600" name="first-name"></ErrorMessage>
    </section>
    <section class="flex flex-col gap-2" id="last-name">
      <Field
        class="w-52 px-2 py-3"
        type="text"
        name="last-name"
        placeholder="Last name"
        v-model="form.last_name"
        :rules="validateName"
        :disabled="!isAuthenticated"
      />
      <ErrorMessage class="text-red-600" name="last-name"></ErrorMessage>
    </section>
    <section class="flex flex-col gap-2" id="participation">
      <Field
        class="w-52 px-2 py-3"
        type="number"
        name="participation"
        placeholder="Participation"
        v-model="form.participation"
        :rules="validateParticipation"
        :disabled="!isAuthenticated"
      />
      <ErrorMessage class="text-red-600" name="participation"></ErrorMessage>
    </section>
    <button
      class="flex place-items-center border-solid border-2 border-white text-white h-10 px-10 font-bold text-sm"
      type="submit"
      :disabled="!isAuthenticated"
    >
      SEND
    </button>
  </VeeForm>
</template>

<script>
import { Form as VeeForm, Field, ErrorMessage } from 'vee-validate'

export default {
  name: 'DataForm',
  props: {
    isAuthenticated: {
      type: Boolean,
      required: true
    }
  },
  components: {
    VeeForm,
    Field,
    ErrorMessage
  },
  data() {
    return {
      form: {
        first_name: '',
        last_name: '',
        participation: null
      }
    }
  },
  methods: {
    submitForm() {
      this.form.participation = parseInt(this.form.participation)

      this.$emit('form-submitted', this.form)
      this.form.first_name = ''
      this.form.last_name = ''
      this.form.participation = null
    },
    validateName(value) {
      if (!value) {
        return 'This field is required'
      }

      if (value != value.trim()) {
        return 'No leading or trailing spaces'
      }

      if (!/^[a-zA-ZÀ-ÿ'-]+$/.test(value)) {
        return 'Please enter a valid name (letters only)'
      }

      return true
    },
    validateParticipation(value) {
      if (!value) {
        return 'This field is required'
      }

      if (!/^\d+$/.test(value)) {
        return 'Please enter a positive integer'
      }

      return true
    }
  }
}
</script>
