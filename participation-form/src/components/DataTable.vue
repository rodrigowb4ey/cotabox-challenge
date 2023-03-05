<template>
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
    <transition-group class="fade" name="fade" tag="tbody">
      <tr v-for="(participant, index) in participants" :key="index">
        <td class="border border-slate-400 py-0 px-3 text-center">{{ participant.id }}</td>
        <td class="border border-slate-400 p-2 py-0">{{ participant.firstName }}</td>
        <td class="border border-slate-400 p-2">{{ participant.lastName }}</td>
        <td class="border border-slate-400 py-2 text-center">
          {{ participant.participation }}
        </td>
      </tr>
    </transition-group>
  </table>
</template>

<script>
export default {
  name: 'DataTable',
  props: {
    participants: {
      type: Object,
      required: true
    }
  }
}
</script>
