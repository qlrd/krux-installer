import { Ref } from "vue"

/**
 * Pick a file to be signed
 * @param page 
 * @returns Function
 */
export default function (
  data: Ref<Record<string, any>>
): Function { 
  return function (_: Event, result: Record<'from' | 'clickMessage' | 'filepath' | 'picked', string>): void {
    if (result.from === 'SignOrVerify::filePicker') {
      data.value.clickMessage = result.clickMessage 
      data.value.filepath = result.filepath
      data.value.picked = result.picked
    }
  }
}