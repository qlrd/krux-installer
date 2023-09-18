<template>
  <v-item-group id="sign-or-verify-file-page">
    <v-container>
      <v-row>
        <v-col
          id="sign-or-verify-page-message-text"
          v-html="clickMessage"
        >
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-item v-slot="{ selectedClass }">
            <v-card
              variant="outlined"
              :class="selectedClass"
              @click.prevent="filePicker"
              id="sign-or-verify-page-choose-file-button"
            >
              <v-card-title
                id="sign-or-verify-page-choose-file-button-text"
              >
                Choose file
              </v-card-title>
            </v-card>
          </v-item>
        </v-col>
      </v-row>
      <v-row v-if="picked">
        <v-col>
          <v-item v-slot="{ selectedClass }">
            <v-card
              variant="outlined"
              :class="selectedClass"
              @click.prevent="fileSigner"
              id="sign-or-verify-page-sign-file-button"
            >
              <v-card-title
                id="sign-or-verify-page-sign-file-button-text"
              >
                Sign {{ filepath }} 
              </v-card-title>
            </v-card>
          </v-item>
        </v-col>
      </v-row>
    </v-container>
  </v-item-group>
</template>

<script setup lang="ts">
import { toRefs, onMounted } from 'vue';

const props = defineProps<{
  clickMessage: string,
  filepath: string
  picked: string
}>()

const { clickMessage, filepath, picked } = toRefs(props)

async function filePicker () {
  await window.api.invoke('krux:file:picker', { from: 'SignOrVerify::filePicker' })
}

async function fileSigner () {
  await window.api.invoke('krux:file:signer')
}

</script>
