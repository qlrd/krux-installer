/// <reference path="../typings/index.d.ts"/>

import ElectronStore from 'electron-store'
import Handler from './handler'
import { dialog } from 'electron'
import { homedir } from 'os'

export default class FilePicker extends Handler {

  constructor (win: Electron.BrowserWindow, storage: ElectronStore, ipcMain: Electron.IpcMain) {
    super('krux:file:picker', win, storage, ipcMain);
  }

  /**
   * Builds a `handle` method for `ipcMain` to be called
   * with `invoke` method in `ipcRenderer`.
   * 
   * @example
   * ```
   * // change some key in store
   * // some keys are forbidden to change
   * // https://api.github.com/repos/selfcustody/krux/git/refs/tags
   * methods: {
   *  async download () {
   *    await window.api.invoke('krux:store:set')
   *    
   *    window.api.onSuccess('krux:store:set', function(_, isChanged) {
   *      // ... do something
   *    }) 
   *
   *    window.api.onError('krux:store:set', function(_, error) {
   *      // ... do something
   *    }) 
   *  } 
   * }
   * 
   * ```
   */
  build () {
    super.build(async (options: Record<'from', string>) => {
      if (options.from === 'SignOrVerify::filePicker') {
        const result = await dialog.showOpenDialog({
          title: 'Choose a file to be signed',
          defaultPath: homedir(), 
          properties: [
            'openFile'
          ]
        })
        if (!result.canceled) {
          this.send(`${this.name}:success`, {
            from: options.from,
            clickMessage: `Click in <span style="color:green;">Sign ${result.filePaths[0]}</span>`, 
            filepath: result.filePaths[0],
            picked: true
          })
        } else {
          this.send(`${this.name}:success`, {
            from: options.from,
            filepath: '',
            clickMessage: 'Choose a file to sign',
            picked: false
          })
        }
      } else {
        const error = new Error(`Forbidden: cannot pick a file from ${options.from}`)
        this.send(`${this.name}:error`, {
          name: error.name,
          message: error.message
        })
      }
    })
  }
}