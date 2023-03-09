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
    async removeParticipantFromList(id) {
      const index = this.participants.findIndex((participant) => participant.id == id)

      this.participants.splice(index, 1)
    },
    randomHexColor() {
      const color = Math.floor(Math.random() * 16777215).toString(16)
      return `#${'0'.repeat(6 - color.length)}${color.toUpperCase()}`
    },
    async addParticipant(participant) {
      try {
        const response = await axios.post('http://localhost:8000/api/participants/', participant, {
          headers: {
            Authorization:
              'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc4MzIxNzc2LCJpYXQiOjE2NzgzMjE0NzYsImp0aSI6ImNiY2ZmODg3YTBlYzRlNzk5YTdlYjg0NDU0N2ZmZjIzIiwidXNlcl9pZCI6MX0.leE-nid98y72eMARjzJAkEOTljml-Hg46ufnQRo0aJU'
          }
        })

        if (response.status == 201) {
          this.participants.push(response.data)
          this.chartData.datasets[0].backgroundColor.push(this.randomHexColor())
        }
      } catch (error) {
        console.error(error)
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
