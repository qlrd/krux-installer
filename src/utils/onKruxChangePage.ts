import { Ref } from "vue"

/**
 * Simple function to change pages
 * @param page 
 * @returns Function
 */
export default function (
  data: Ref<Record<string, any>>,
  page: Ref<string>
): Function {
  return function (_: Event, result: Record<'from' | 'page', string>) {
    if (result.from === 'KruxInstallerLogo') {
      delete data.value.messages
      delete data.value.indexes
    }
    
    page.value = result.page

    if (page.value === 'SignOrVerify') {
      data.value.clickMessage = 'Choose a file to sign'
    }
  }
}