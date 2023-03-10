<template>
  <VeeForm @submit="login">
    <section class="mb-4">
      <label for="username" class="block text-gray-700 font-bold mb-2">Username:</label>
      <Field
        type="text"
        id="username"
        name="username"
        v-model="loginForm.username"
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
        v-model="loginForm.password"
        placeholder="Enter your password"
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
        Login
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
      loginForm: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('/api/auth/login/', this.loginForm)
        if (response.status == 200) {
          const accessToken = response.data['access_token']

          localStorage.setItem('access_token', accessToken)
          console.log(localStorage)
          this.$swal.fire({
            title: 'Logged in!',
            icon: 'success',
            timer: 1000,
            timerProgressBar: true
          })
          this.$emit('login-form-closed', true)
          this.clearLoginForm()
        }
      } catch (error) {
        console.error(error)
      }
    },
    clearLoginForm() {
      this.loginForm.username = ''
      this.loginForm.password = ''
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

      return true
    }
  }
}
</script>
