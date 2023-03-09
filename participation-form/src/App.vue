<template>
  <header class="flex gap-8 items-center justify-center bg-cyan-500">
    <DataForm :is-authenticated="isAuthenticated" @form-submitted="addParticipant"></DataForm>
    <nav v-if="!isAuthenticated" class="flex items-center justify-end px-4 py-2 bg-gray-800">
      <button @click="showLoginModal = true" class="text-white text-sm mr-4">Login</button>
      <button @click="showRegisterModal = true" class="text-white text-sm">Register</button>
    </nav>
    <nav v-else class="flex items-center justify-end px-4 py-2 bg-gray-800">
      <button @click="logout" class="text-white text-sm">Logout</button>
    </nav>
  </header>
  <main class="flex items-center justify-center align-middle flex-col">
    <div v-if="showLoginModal">
      <div class="modal-overlay" @click="showLoginModal = false"></div>
      <div class="modal-container">
        <div class="modal-content">
          <LoginForm @login-form-closed="closeLoginModal"></LoginForm>
        </div>
      </div>
    </div>
    <div v-if="showRegisterModal">
      <div class="modal-overlay" @click="showRegisterModal = false"></div>
      <div class="modal-container">
        <div class="modal-content">
          <RegisterForm @register-form-closed="closeRegisterModal"></RegisterForm>
        </div>
      </div>
    </div>
    <h1 class="mt-10 font-bold text-gray-600 text-2xl">PARTICIPATION DATA</h1>
    <h2 class="pt-5 text-[14px] text-gray-700 pb-10">Keeping track of the %.</h2>
    <section id="data-display" class="flex items-center justify-center gap-x-28 w-full">
      <section id="data-table">
        <DataTable
          :participants="participants"
          :totalParticipations="totalNumOfParticipations"
          @participant-deleted="removeParticipantFromList"
        ></DataTable>
      </section>
      <section id="data-chart">
        <Doughnut ref="chart" :data="chartData" :key="chartKey" />
      </section>
    </section>
  </main>
</template>

<script>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'vue-chartjs'
import DataTable from './components/DataTable.vue'
import DataForm from './components/DataForm.vue'
import LoginForm from './components/LoginForm.vue'
import RegisterForm from './components/RegisterForm.vue'
import axios from 'axios'

ChartJS.register(ArcElement, Tooltip, Legend)
ChartJS.defaults.plugins.legend.position = 'right'

export default {
  name: 'App',
  components: {
    Doughnut,
    DataTable,
    DataForm,
    LoginForm,
    RegisterForm
  },
  data() {
    return {
      isAuthenticated: localStorage.getItem('access_token') ? true : false,
      showLoginModal: false,
      showRegisterModal: false,
      participants: [],
      chartKey: 0,
      chartData: {
        labels: [],
        datasets: [
          {
            backgroundColor: [],
            data: []
          }
        ]
      }
    }
  },
  computed: {
    totalNumOfParticipations() {
      let sum = 0

      if (this.participants.length > 0) {
        this.participants.forEach((participant) => {
          sum += participant.participation
        })
      }

      return sum
    }
  },
  watch: {
    chartData: {
      handler() {
        this.chartKey += 1
      },
      deep: true
    },
    participants: {
      handler() {
        this.updateChartData(this.participants)
      },
      deep: true
    }
  },
  methods: {
    async logout() {
      let accessToken = localStorage.getItem('access_token')

      console.log(accessToken)

      try {
        const response = await axios.post('http://localhost:8000/api/auth/logout/', {
          headers: {
            Authorization: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4MzkxNTY1LCJpYXQiOjE2NzgzOTEyNjUsImp0aSI6IjUzNWQ3NDJkYzI3ZTRkYWJhY2VmNWU3ZDk3Mzg4ODUzIiwidXNlcl9pZCI6MX0.Uwx1WGYnLOqGfQ--FNWRndv4VdbMMjR4_SEFv3uIgvM`
          }
        })

        if (response.status == 200) {
          localStorage.removeItem('access_token')
          this.$swal.fire({
            title: 'Logged out!',
            icon: 'success',
            timer: 1000,
            timerProgressBar: true
          })
          this.isAuthenticated = false
        }
      } catch (error) {
        console.error(error)
      }
    },
    closeRegisterModal() {
      this.showRegisterModal = false
      this.isAuthenticated = true
    },
    closeLoginModal() {
      this.showLoginModal = false
      this.isAuthenticated = true
    },
    async removeParticipantFromList(id) {
      const index = this.participants.findIndex((participant) => participant.id == id)

      this.participants.splice(index, 1)
    },
    randomHexColor() {
      const color = Math.floor(Math.random() * 16777215).toString(16)
      return `#${'0'.repeat(6 - color.length)}${color.toUpperCase()}`
    },
    async addParticipant(participant) {
      let accessToken = localStorage.getItem('access_token')

      try {
        const response = await axios.post('http://localhost:8000/api/participants/', participant, {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        })

        if (response.status == 201) {
          this.participants.push(response.data)
          this.chartData.datasets[0].backgroundColor.push(this.randomHexColor())
        }
      } catch (error) {
        console.error(error)
        this.$swal.fire({
          title: 'Unauthorized',
          icon: 'error',
          timer: 1000,
          timerProgressBar: true
        })
      }
    },
    updateChartData(participants) {
      this.chartData.labels = participants.map(
        (participant) => `${participant.first_name} ${participant.last_name}`
      )

      this.chartData.datasets[0].data = participants.map((participant) => participant.participation)
    },
    updateChart() {
      const noDataYet = this.chartData.labels.find((label) => label === 'No data yet')

      if (noDataYet) {
        this.chartData.datasets[0].backgroundColor = []
      }

      this.updateChartData(this.participants)

      this.chartData.datasets[0].backgroundColor.push(this.randomHexColor())
    }
  },
  async created() {
    try {
      const response = await axios.get('http://localhost:8000/api/participants')

      if (response.data.length > 0) {
        this.updateChartData(response.data)
        this.participants = response.data
        response.data.forEach(() => {
          this.chartData.datasets[0].backgroundColor.push(this.randomHexColor())
        })
      } else {
        this.chartData.labels = ['No data yet']
        this.chartData.datasets[0].data = [1]
        this.chartData.datasets[0].backgroundColor.push(this.randomHexColor())
      }
    } catch (error) {
      console.error(error)
    }
  }
}
</script>

<style>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

.modal-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  padding: 1rem;
}
</style>
