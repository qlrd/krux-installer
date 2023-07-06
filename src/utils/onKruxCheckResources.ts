import { Ref } from "vue"
import messages from "./messages"

async function onResourceExist (
  data: Ref<Record<string, any>>,
  result: Record<'from' | 'exists' | 'baseUrl' | 'resourceFrom' | 'resourceTo', any>
) {
  await messages.add(data, `${result.resourceTo} found`)
  data.value.proceedTo = 'ConsoleLoad'
  data.value.backTo = 'GithubChecker'
  await messages.close(data)
  await window.api.invoke('krux:change:page', { page: 'WarningDownload' })
}

async function onResourceNotExist (
  data: Ref<Record<string, any>>,
  result: Record<'from' | 'exists' | 'baseUrl' | 'resourceFrom' | 'resourceTo', any>,
  page: string
) {
  await messages.add(data, `${result.resourceTo} not found`)
  data.value.progress = 0.0
  await messages.close(data)
  await window.api.invoke('krux:change:page', { page: page })
}

export default function (data: Ref<Record<string, any>>): Function {
  return async function (
    _: Event,
    result: Record<'from' | 'exists' | 'baseUrl' | 'resourceFrom' | 'resourceTo', any>
  ): Promise<void> {
    data.value.baseUrl = result.baseUrl
    data.value.resourceFrom = result.resourceFrom
    data.value.resourceTo = result.resourceTo

    // When user decides between official
    // or test releaases
    if (result.from === 'SelectVersion' ) { 
      if (result.exists) {
        await onResourceExist(data, result)
      } else {
        if (result.baseUrl.match(/selfcustody/g)) {
          await onResourceNotExist(data, result, 'DownloadOfficialReleaseZip')
        }
        if (result.resourceFrom.match(/odudex\/krux_binaries/g)){
          await onResourceNotExist(data, result, 'DownloadTestFirmware')
        }
      }
    }

    // When user decides for official release
    // and checked zip file to redirect to sha256.txt file
    if (
      result.from === 'DownloadOfficialReleaseZip' ||
      result.from.match(/^WarningDownload::.*.zip$/)
    ) {
      if (result.exists) {
        await onResourceExist(data, result)
      } else {
        await onResourceNotExist(data, result, 'DownloadOfficialReleaseSha256')
      }
    }

    // When user decides for official release
    // and checked zip.sha256.txt file to redirect to zip.sig file
    if (
      result.from === 'DownloadOfficialReleaseSha256' ||
      result.from.match(/^WarningDownload::.*.zip.sha256.txt$/)
    ) {
      if (result.exists) {
        await onResourceExist(data, result)
      } else {
        await onResourceNotExist(data, result, 'DownloadOfficialReleaseSig')
      }
    }

    // When user decides for official release
    // and checked zip.sig file to redirect to .pem file
    if (
      result.from === 'DownloadOfficialReleaseSig' ||
      result.from.match(/^WarningDownload::.*.zip.sig$/)
    ) {
      if (result.exists) {
        await onResourceExist(data, result)
      } else {
        await onResourceNotExist(data, result, 'DownloadOfficialReleasePem')
      }
    }

    if (result.from === 'CheckVerifyOfficialRelease') {
      data.value = {}
    }

    if (
      result.from === 'DownloadTestFirmware' ||
      result.from.match(/^WarningDownload::.*firmware.bin$/)
    ) {
      if (result.exists) {
        await onResourceExist(data, result)
      } else {
        await onResourceNotExist(data, result, 'DownloadTestKboot')
      }
    }

    if (
      result.from === 'DownloadTestKboot' ||
      result.from.match(/^WarningDownload::.*kboot.kfpkg$/)
    ) {
      if (result.exists) {
        await onResourceExist(data, result)
      } else {
        await onResourceNotExist(data, result, 'DownloadTestKtool')
      }
    }

    if (
      result.from === 'DownloadTestKtool' ||
      result.from.match(/^WarningDownload::.*ktool-(linux|win.exe|mac|mac-10)$/)
    ) {
      if (result.exists) {
        await onResourceExist(data, result)
      } else {
        await onResourceNotExist(data, result, 'Main')
      }
    }
  }
}