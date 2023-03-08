<template>
  <header class="flex items-center justify-center bg-cyan-500">
    <DataForm @form-submitted="addParticipant"></DataForm>
  </header>
  <main class="flex items-center justify-center align-middle flex-col">
    <h1 class="mt-10 font-bold text-gray-600 text-2xl">PARTICIPATION DATA</h1>
    <h2 class="pt-5 text-[14px] text-gray-700 pb-10">Keeping track of the %.</h2>
    <section id="data-display" class="flex items-center justify-center gap-x-28 w-full">
      <section id="data-table">
        <DataTable
          :participants="participants"
          :totalParticipations="totalNumOfParticipations"
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
import axios from 'axios'

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
        first_name: participant.first_name,
        last_name: participant.last_name,
        participation: participant.participation
      }

      this.participants.push(newParticipant)

      this.updateChart()
    },
    updateChartData(participants) {
      console.log('peraimah', participants)

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

      this.updateChartData(response.data)

      response.data.forEach(() => {
        this.chartData.datasets[0].backgroundColor.push(this.randomHexColor())
      })

      this.participants = response.data
    } catch (error) {
      console.error(error)
    }
  }
}
</script>
