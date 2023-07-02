import { Ref } from "vue"
import addMessage from "./addMessage"

export default function (data: Ref<Record<string, any>>): Function {
  return async function (
    _: Event,
    result: Record<'from' | 'exists' | 'baseUrl' | 'resourceFrom' | 'resourceTo', any>
  ): Promise<void> {
    data.value.baseUrl = result.baseUrl
    data.value.resourceFrom = result.resourceFrom
    data.value.resourceTo = result.resourceTo

    if (result.from === 'SelectVersion' ) { 
      if (result.exists) {
        await addMessage(data, `${result.resourceTo} found`)
        data.value.proceedTo = 'CheckResourcesOfficialReleaseSha256'
        data.value.backTo = 'GithubChecker'
        await window.api.invoke('krux:change:page', { page: 'WarningDownload' })
      } else {
        await addMessage(data, `${result.resourceTo} not found`)
        data.value.progress = 0.0
        if (result.baseUrl.match(/selfcustody/g)) {
          await window.api.invoke('krux:change:page', { page: 'DownloadOfficialReleaseZip' })
        }
        if (result.resourceFrom.match(/odudex\/krux_binaries/g)){
          await window.api.invoke('krux:change:page', { page: 'DownloadTestFirmware' })
        }
      }
    }

    if (result.from === 'CheckResourcesOfficialReleaseZip' ) { 
      if (result.exists) {
        data.value.proceedTo = 'CheckResourcesOfficialReleaseSha256'
        data.value.backTo = 'GithubChecker'
        await window.api.invoke('krux:change:page', { page: 'WarningDownload' })
      } else {
        data.value.progress = 0.0
        await window.api.invoke('krux:change:page', { page: 'DownloadOfficialReleaseZip' })
      }
    }

    if (result.from === 'CheckResourcesOfficialReleaseSha256' ) { 
      if (result.exists) {
        data.value.proceedTo = 'CheckResourcesOfficialReleaseSig'
        data.value.backTo = 'GithubChecker'
        await window.api.invoke('krux:change:page', { page: 'WarningDownload' })
      } else {
        data.value.progress = 0.0
        await window.api.invoke('krux:change:page', { page: 'DownloadOfficialReleaseSha256' })
      }
    }

    if (result.from === 'CheckResourcesOfficialReleaseSig' ) { 
      if (result.exists) {
        data.value.proceedTo = 'CheckResourcesOfficialReleasePem'
        data.value.backTo = 'GithubChecker'
        await window.api.invoke('krux:change:page', { page: 'WarningDownload' })
      } else {
        data.value.progress = 0.0
        await window.api.invoke('krux:change:page', { page: 'DownloadOfficialReleaseSig' })
      }
    }

    if (result.from === 'CheckResourcesOfficialReleasePem' ) { 
      if (result.exists) {
        data.value.proceedTo = 'CheckVerifyOfficialRelease'
        data.value.backTo = 'GithubChecker'
        await window.api.invoke('krux:change:page', { page: 'WarningDownload' })
      } else {
        data.value.progress = 0.0
        await window.api.invoke('krux:change:page', { page: 'DownloadOfficialReleasePem' })
      }
    }

    if (result.from === 'CheckVerifyOfficialRelease') {
      data.value = {}
    }

    if (result.from === 'CheckResourcesTestFirmware') {
      if (result.exists) {
        data.value.proceedTo = 'CheckResourcesTestKboot'
        data.value.backTo = 'GithubChecker'
        await window.api.invoke('krux:change:page', { page: 'WarningDownload' })
      } else {
        data.value.progress = 0.0
        await window.api.invoke('krux:change:page', { page: 'DownloadTestFirmware' })
      }
    }

    if (result.from === 'CheckResourcesTestKboot') {
      if (result.exists) {
        data.value.proceedTo = 'CheckResourcesTestKtool'
        data.value.backTo = 'GithubChecker'
        await window.api.invoke('krux:change:page', { page: 'WarningDownload' })
      } else {
        data.value.progress = 0.0
        await window.api.invoke('krux:change:page', { page: 'DownloadTestKboot' })
      }
    }

    if (result.from === 'CheckResourcesTestKtool') {
      if (result.exists) {
        data.value.proceedTo = 'Main'
        data.value.backTo = 'GithubChecker'
        await window.api.invoke('krux:change:page', { page: 'WarningDownload' })
      } else {
        data.value.progress = 0.0
        await window.api.invoke('krux:change:page', { page: 'DownloadTestKtool' })
      }
    }

    if (result.from === 'WarningDownload') {
      data.value = {
        baseUrl: result.baseUrl,
        resourceFrom: result.resourceFrom,
        resourceTo: result.resourceTo,
        progress: 0.0
      }
      let page = ''
      if (result.resourceFrom.match(/zip$/g)) {
        await window.api.invoke('krux:change:page', { page: 'DownloadOfficialReleaseZip' })
      }
      else if (result.resourceFrom.match(/zip.sha256.txt$/g)) {
        await window.api.invoke('krux:change:page', { page: 'DownloadOfficialReleaseSha256' })
      }
      else if (result.resourceFrom.match(/zip.sig$/g)) {
        await window.api.invoke('krux:change:page', { page: 'DownloadOfficialReleaseSig' })
      }
      else if (result.resourceFrom.match(/pem$/g)) {
        await window.api.invoke('krux:change:page', { page: 'DownloadOfficialReleasePem' })
      }
      else if (result.resourceFrom.match(/bin$/g)) {
        await window.api.invoke('krux:change:page', { page: 'DownloadTestFirmware' })
      }
      else if (result.resourceFrom.match(/kfpkg$/g)) {
        await window.api.invoke('krux:change:page', { page: 'DownloadTestKboot' })
      }
      else if (result.resourceFrom.match(/^ktool/g)) {
        await window.api.invoke('krux:change:page', { page: 'DownloadTestKtool' })
      }
      else {
        data.value = {
          stack: new Error(`Invalid resource: ${result.resourceFrom}`)
        }
        await window.api.invoke('krux:change:page', { page: 'ErrorMsg' })
      }
    }
  }
}