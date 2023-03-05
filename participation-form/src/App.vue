<template>
  <header class="flex items-center justify-center bg-cyan-500">
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
  </header>
  <main class="flex items-center justify-center align-middle flex-col">
    <h1 class="mt-10 font-bold text-gray-600 text-2xl">PARTICIPATION DATA</h1>
    <h2 class="pt-5 text-[14px] text-gray-700">Keeping track of the %.</h2>
    <section id="data-display" class="flex items-center justify-center gap-x-28 w-full">
      <section id="data-table">
        <DataTable :participants="participants"></DataTable>
      </section>
      <section id="data-graph">
        <Doughnut ref="chart" :data="chartData" :key="chartKey" />
      </section>
    </section>
  </main>
</template>

<script>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'vue-chartjs'
import DataTable from './components/DataTable.vue'

ChartJS.register(ArcElement, Tooltip, Legend)
ChartJS.defaults.plugins.legend.position = 'right'

export default {
  name: 'App',
  components: {
    Doughnut,
    DataTable
  },
  data() {
    return {
      chartKey: 0,
      form: {
        firstName: '',
        lastName: '',
        participation: null
      },
      participants: [],
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
  watch: {
    chartData: {
      handler() {
        this.chartKey += 1
      },
      deep: true
    }
  },
  methods: {
    randomHexColor() {
      const color = Math.floor(Math.random() * 16777215).toString(16)
      return `#${'0'.repeat(6 - color.length)}${color.toUpperCase()}`
    },
    updateChart() {
      const noDataYet = this.chartData.labels.find((label) => label === 'No data yet')

      if (noDataYet) {
        this.chartData.datasets[0].backgroundColor = []
      }

      this.chartData.labels = this.participants.map(
        (participant) => `${participant.firstName} ${participant.lastName}`
      )

      this.chartData.datasets[0].data = this.participants.map(
        (participant) => participant.participation
      )

      this.chartData.datasets[0].backgroundColor.push(this.randomHexColor())
    },
    submitForm() {
      const newParticipant = {
        id: this.participants.length + 1,
        firstName: this.form.firstName,
        lastName: this.form.lastName,
        participation: this.form.participation
      }

      this.participants.push(newParticipant)

      this.form.firstName = ''
      this.form.lastName = ''
      this.form.participation = null

      this.updateChart()
    }
  },
  created() {
    this.chartData.labels.push('No data yet')
    this.chartData.datasets[0].data.push(1)
    this.chartData.datasets[0].backgroundColor.push('#964B00')
  }
}
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to {
  opacity: 1;
  animation: fade-in 0.5s;
}
</style>
