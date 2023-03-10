<template>
  <VeeForm @submit="register">
    <section class="mb-4">
      <label for="username" class="block text-gray-700 font-bold mb-2">Username:</label>
      <Field
        type="text"
        id="username"
        name="username"
        v-model="registerForm.username"
        placeholder="Enter your username"
        class="border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        :rules="validateUsername"
      />
      <ErrorMessage class="text-red-600" name="username"></ErrorMessage>
    </section>
    <section class="mb-4">
      <label for="password" class="block text-gray-700 font-bold mb-2">Password:</label>
      <Field
        type="password"
        id="password"
        name="password"
        v-model="registerForm.password1"
        placeholder="Enter your password"
        class="border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        :rules="validatePassword"
      />
      <ErrorMessage class="text-red-600" name="password"></ErrorMessage>
    </section>
    <section class="mb-4">
      <label for="confirm-password" class="block text-gray-700 font-bold mb-2"
        >Confirm password:</label
      >
      <Field
        type="password"
        id="confirm-password"
        name="confirm-password"
        v-model="registerForm.password2"
        placeholder="Confirm your password"
        class="border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        :rules="validatePassword"
      />
      <ErrorMessage class="text-red-600" name="password"></ErrorMessage>
    </section>
    <section class="flex items-center justify-between">
      <button
        type="submit"
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      >
        Register
      </button>
    </section>
  </VeeForm>
</template>

<script>
import { Form as VeeForm, Field, ErrorMessage } from 'vee-validate'
import axios from 'axios'

export default {
  name: 'LoginForm',
  components: {
    VeeForm,
    Field,
    ErrorMessage
  },
  data() {
    return {
      registerForm: {
        username: '',
        password1: '',
        password2: ''
      }
    }
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('/api/auth/register/', this.registerForm)
        if (response.status == 201) {
          const accessToken = response.data['access_token']

          localStorage.setItem('access_token', accessToken)
          console.log(localStorage)
          this.$swal.fire({
            title: 'Registered and Logged in!',
            icon: 'success',
            timer: 1000,
            timerProgressBar: true
          })
          this.$emit('register-form-closed', true)
          this.clearRegisterForm()
        }
      } catch (error) {
        let errorMessage = ''

        const errors = error.response.data

        for (const key in errors) {
          const messages = errors[key]
          errorMessage += '\n' + messages.join(', ')
        }

        this.$swal.fire({
          title: 'Unauthorized',
          text: errorMessage,
          icon: 'error',
          timer: 2000,
          timerProgressBar: true
        })
      }
    },
    clearRegisterForm() {
      this.registerForm.username = ''
      this.registerForm.password1 = ''
      this.registerForm.password2 = ''
    },
    validateUsername(value) {
      if (!value) {
        return 'This field is required'
      }

      if (value != value.trim()) {
        return 'No leading or trailing spaces'
      }

      return true
    },
    validatePassword(value) {
      if (!value) {
        return 'This field is required'
      }

      if (value != value.trim()) {
        return 'No leading or trailing spaces'
      }

      if (value.length < 8) {
        return 'Password must contain at least 8 characters'
      }

      return true
    }
  }
}
</script>
