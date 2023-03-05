<template>
  <form class="flex gap-5 py-10 text-xs" @submit.prevent="submitForm">
    <input
      class="w-52 px-2 py-3"
      type="text"
      id="first-name"
      name="first-name"
      placeholder="First name"
      v-model="form.firstName"
    />
    <input
      class="w-52 px-2 py-3"
      type="text"
      id="last-name"
      name="last-name"
      placeholder="Last name"
      v-model="form.lastName"
    />
    <input
      class="w-52 px-2 py-3"
      type="number"
      id="participation"
      name="participation"
      placeholder="Participation"
      v-model="form.participation"
    />
    <button
      class="flex place-items-center border-solid border-2 border-white text-white font-bold px-10 text-sm"
      type="submit"
    >
      SEND
    </button>
  </form>
</template>

<script>
export default {
  name: 'DataForm',
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
      this.$emit('form-submitted', this.form)
      this.form.firstName = ''
      this.form.lastName = ''
      this.form.participation = null
    }
  }
}
</script>
