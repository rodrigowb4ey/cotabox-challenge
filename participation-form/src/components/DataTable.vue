<template>
  <table class="border-collapse border border-slate-400 text-slate-600 text-[10px]">
    <colgroup>
      <col class="w-5" />
      <col class="w-44" span="2" />
      <col class="w-15" />
      <col class="w-5" />
    </colgroup>
    <thead>
      <tr>
        <th class="border border-slate-400 p-2">&nbsp;</th>
        <th class="border border-slate-400 p-2 text-left">First name</th>
        <th class="border border-slate-400 p-2 text-left">Last name</th>
        <th class="border border-slate-400 py-2 px-4">Participation</th>
        <th class="p-2">&nbsp;</th>
      </tr>
    </thead>
    <transition-group class="fade" name="fade" tag="tbody">
      <tr v-for="(participant, index) in participants" :key="index">
        <td class="border border-slate-400 py-0 px-3 text-center">{{ participant.id }}</td>
        <td class="border border-slate-400 p-2 py-0">{{ participant.first_name }}</td>
        <td class="border border-slate-400 p-2">{{ participant.last_name }}</td>
        <td class="border border-slate-400 py-2 text-center">
          {{ ((participant.participation / totalParticipations) * 100).toFixed(2) }}%
        </td>
        <td class="border border-slate-400 py-2 px-4">
          <button @click="removeParticipant(participant.id)">
            <font-awesome-icon icon="fas fa-trash-alt"></font-awesome-icon>
          </button>
        </td>
      </tr>
    </transition-group>
  </table>
</template>

<script>
import axios from 'axios'

export default {
  name: 'DataTable',
  props: {
    participants: {
      type: Object,
      required: true
    },
    totalParticipations: {
      type: Number,
      required: true
    }
  },
  methods: {
    async removeParticipant(id) {
      let accessToken = localStorage.getItem('access_token')
      try {
        const response = await axios.delete(`/api/participants/${id}/`, {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        })

        if (response.status == 204) {
          this.$emit('participant-deleted', id)
          console.log(response)
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
    }
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
