<template>
  <VeeForm class="flex gap-5 py-10 text-xs" @submit="submitForm">
    <section class="flex flex-col gap-2" id="first-name">
      <Field
        class="w-52 px-2 py-3"
        type="text"
        name="first-name"
        placeholder="First name"
        v-model="form.firstName"
        :rules="validateName"
      />
      <ErrorMessage class="text-red-600" name="first-name"></ErrorMessage>
    </section>
    <section class="flex flex-col gap-2" id="last-name">
      <Field
        class="w-52 px-2 py-3"
        type="text"
        name="last-name"
        placeholder="Last name"
        v-model="form.lastName"
        :rules="validateName"
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
      />
      <ErrorMessage class="text-red-600" name="participation"></ErrorMessage>
    </section>
    <button
      class="flex place-items-center border-solid border-2 border-white text-white font-bold px-10 text-sm"
      type="submit"
    >
      SEND
    </button>
  </VeeForm>
</template>

<script>
import { Form as VeeForm, Field, ErrorMessage } from 'vee-validate'

export default {
  name: 'DataForm',
  components: {
    VeeForm,
    Field,
    ErrorMessage
  },
  data() {
    return {
      form: {
        firstName: '',
        lastName: '',
        participation: null
      }
    }
  },
  methods: {
    submitForm() {
      this.form.participation = parseInt(this.form.participation)

      this.$emit('form-submitted', this.form)
      this.form.firstName = ''
      this.form.lastName = ''
      this.form.participation = null
    },
    validateName(value) {
      if (!value) {
        return 'This field is required'
      }

      if (!/^[a-zA-Z]+$/.test(value)) {
        return 'Please enter a valid name (letters only)'
      }

      return true
    },
    validateParticipation(value) {
      if (!value) {
        return 'This field is required'
      }

      if (!/^\d+$/.test(value)) {
        return 'Please enter a valid integer'
      }

      return true
    }
  }
}
</script>
