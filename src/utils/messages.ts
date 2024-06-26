import { Ref } from "vue"
import delay from "./delay"

async function add(
  data: Ref<Record<string, any>>,
  message: string
): Promise<void> {
  data.value.messages.push(message)
  data.value.indexes.push(0)
  await delay(10)
  data.value.indexes[data.value.indexes.length - 1] += 1
  await delay(3000)
}

function clean(data: Ref<Record<string, any>>): void {
  data.value.messages = []
  data.value.indexes = []
  data.value.output = ""
  data.value.done = false
}

async function close(data: Ref<Record<string, any>>): Promise<void> {
  for(let i in data.value.indexes) {
    data.value.indexes[i] = 2
    await delay(100)
  }
}

export default { add, clean, close }
