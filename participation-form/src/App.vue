<template>
  <header class="flex items-center justify-center bg-cyan-500">
    <DataForm @form-submitted="addParticipant"></DataForm>
  </header>
  <main class="flex items-center justify-center align-middle flex-col">
    <h1 class="mt-10 font-bold text-gray-600 text-2xl">PARTICIPATION DATA</h1>
    <h2 class="pt-5 text-[14px] text-gray-700">Keeping track of the %.</h2>
    <section id="data-display" class="flex items-center justify-center gap-x-28 w-full">
      <section id="data-table">
        <DataTable :participants="participants"></DataTable>
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

ChartJS.register(ArcElement, Tooltip, Legend)
ChartJS.defaults.plugins.legend.position = 'right'

export default {
  name: 'App',
  components: {
    Doughnut,
    DataTable,
    DataForm
  },
  data() {
    return {
      participants: [],
      chartKey: 0,
      chartData: {
        labels: ['No data yet'],
        datasets: [
          {
            backgroundColor: ['#964B00'],
            data: [1]
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
    addParticipant(participant) {
      const newParticipant = {
        id: this.participants.length + 1,
        firstName: participant.firstName,
        lastName: participant.lastName,
        participation: participant.participation
      }

      this.participants.push(newParticipant)

      this.updateChart()
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
    }
  }
}
</script>
