<template>
  <v-layout row wrap>
    <v-flex xs12>
      <v-card class="ma-5 pa-5">
        <v-card-title>
          Flash to device
        </v-card-title>
        <v-card-subtitle><b>version</b>: {{ version }}</v-card-subtitle> 
        <v-card-subtitle><b>device</b>: {{ device }}</v-card-subtitle>
        <v-card-content>
          <v-card-text v-for="(text, i) in texts" :key="i">
            {{ text }}
          </v-card-text>
        </v-card-content>
        <v-card-actions>
          <v-btn @click.prevent="$emit('onSuccess', { page: 'WriteFirmwareToDevicePage' })">
            Flash
          </v-btn>
          <v-btn @click.prevent="$emit('onSuccess', { page: 'MainPage' })">
            Back
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>

export default {
  name: 'BeforeFlashDevicePage',
  data () {
    return {
      version: '',
      device: '',
      texts: [
        'Flash to device is required when you intend to install krux for the first time on your device (or for development and testing purposes).',
        'Once you plugged an powered it, click on "flash" button',
      ]
    }
  },
  watch: {
    async version (value) {
      if (value !== '') {
        await window.KruxInstaller.device.get()
      }
    }
  },
  async created () {
    await window.KruxInstaller.version.get()

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.version.onGet((_event, value) => {
      this.version = value
    })

    // eslint-disable-next-line no-unused-vars
    window.KruxInstaller.device.onGet((_event, value) => {
      this.device = value
    })
  }
}
</script>
