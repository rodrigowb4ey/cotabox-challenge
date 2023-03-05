<template>
  <header class="flex items-center justify-center bg-cyan-500">
    <form class="flex gap-5 py-10 text-xs">
      <input
        class="w-52 px-2 py-3"
        type="text"
        id="first-name"
        name="first-name"
        placeholder="First name"
      />
      <input
        class="w-52 px-2 py-3"
        type="text"
        id="last-name"
        name="last-name"
        placeholder="Last name"
      />
      <input
        class="w-52 px-2 py-3"
        type="number"
        id="participation"
        name="participation"
        placeholder="Participation"
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
        <table class="border-collapse border border-slate-400 text-slate-600 text-[10px]">
          <colgroup>
            <col class="w-5" />
            <col class="w-44" span="2" />
            <col class="w-15" />
          </colgroup>
          <thead>
            <tr>
              <th class="border border-slate-400 p-2">&nbsp;</th>
              <th class="border border-slate-400 p-2 text-left">First name</th>
              <th class="border border-slate-400 p-2 text-left">Last name</th>
              <th class="border border-slate-400 py-2 px-4">Participation</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(participant, index) in participants" :key="index">
              <td class="border border-slate-400 py-0 px-3 text-center">{{ participant.id }}</td>
              <td class="border border-slate-400 p-2 py-0">{{ participant.firstName }}</td>
              <td class="border border-slate-400 p-2">{{ participant.lastName }}</td>
              <td class="border border-slate-400 py-2 text-center">
                {{ participant.participation }}
              </td>
            </tr>
          </tbody>
        </table>
      </section>
      <section id="data-graph">
        <Doughnut ref="chart" :data="chartData" />
      </section>
    </section>
  </main>
</template>

<script>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)
ChartJS.defaults.plugins.legend.position = 'right'

export default {
  name: 'App',
  components: {
    Doughnut
  },
  data() {
    return {
      participants: [
        { id: 1, firstName: 'Rodrigo', lastName: 'Bezerra', participation: 30 },
        { id: 2, firstName: 'Andre', lastName: 'Lucas', participation: 20 },
        { id: 3, firstName: 'Jefferson', lastName: 'Moraes', participation: 50 }
      ],
      chartData: {
        labels: [],
        datasets: [
          {
            backgroundColor: ['#41B883', '#E46651', '#00D8FF'],
            data: []
          }
        ]
      }
    }
  },
  methods: {
    updateChart() {
      this.chartData.labels = this.participants.map(
        (participant) => `${participant.firstName} ${participant.lastName}`
      )

      this.chartData.datasets[0].data = this.participants.map(
        (participant) => participant.participation
      )

      this.$refs.chart.update()
    }
  },
  created() {
    this.chartData.labels = this.participants.map(
      (participant) => `${participant.firstName} ${participant.lastName}`
    )

    this.chartData.datasets[0].data = this.participants.map(
      (participant) => participant.participation
    )
  }
}
</script>
