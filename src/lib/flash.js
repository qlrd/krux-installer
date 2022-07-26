'use strict'

import { spawn } from 'child_process'
import { join } from 'path'
// import { userInfo } from 'os'
import Handler from './base'
import Sudoer from '@nathanielks/electron-sudo'

class FlashHandler extends Handler {

  constructor (app, store) {
    super('flash', app, store)

    const resources = this.store.get('resources')
    const version = this.store.get('version')
    this.device = this.store.get('device')

    if (version.match(/selfcustody/g)) {
      this.version = version.split('tag/')[1]
      this.cwd = join(resources, this.version, `krux-${this.version}`)
    }

    if (version.match(/odudex/g)) {
      this.version = join(version, 'raw', 'main')
      this.cwd = join(resources, this.version)
    }
  }

  setup () {
    const os = this.store.get('os')
    const isMac10 = this.store.get('isMac10')

    this.flash = { command: '', args: [] }
    this.chmod = { commands: [] }

    if (os === 'linux') {
      this.flash.command = join(this.cwd, 'ktool-linux')
      this.chmod.commands.push({ command: 'chmod', args: ['+x', this.flash.command] })
    } else if (os === 'darwin' && !isMac10) {
      this.flash.command = join(this.cwd, 'ktool-mac')
      this.chmod.commands.push({ command: 'chmod', args: ['+x', this.flash.command] })
    } else if (os === 'darwin' && isMac10) {
      this.flash.command = join(this.cwd, 'ktool-mac-10')
      this.chmod.commands.push({ command: 'chmod', args: ['+x', this.flash.command] })
    } else if (os === 'win32') {
      this.flash.command = join(this.cwd, 'ktool-win.exe')
      // SEE
      // https://stackoverflow.com/questions/2928738/how-to-grant-permission-to-users-for-a-directory-using-command-line-in-windows
      // https://answers.microsoft.com/en-us/windows/forum/all/what-is-meant-by-no-mapping-between-account-names/dcccb1bb-1c4d-4bd5-91a7-832cabf9c86b)
      // https://www.techinpost.com/no-mapping-between-account-names-and-security-ids-was-done/
      // https://ourtechroom.com/tech/windows-equivalent-to-chmod-command/)
      // this.chmod.commands.push({ command: 'icacls.exe', args: [this.flash.command, '/inheritance:r'] })
      // this.chmod.commands.push({ command: 'icacls.exe', args: [this.flash.command, '/reset'] })
      // this.chmod.commands.push({ command: 'icacls.exe', args: [this.flash.command, '/grant:r', `${userInfo().username}:F`] })
      // this.chmod.commands.push({ command: 'icacls.exe', args: [this.flash.command, '/grant:r', 'Everyone:F'] })
    }

    const kboot = join(this.cwd, this.device, 'kboot.kfpkg')
    this.flash.args = ['-B', 'goE', '-b', '1500000', kboot]
  }

  enable () {
    const promises = this.chmod.commands.map((cmd) => {
      return new Promise((resolve, reject) => {
        const message = `${cmd.command} ${cmd.args.join(' ')}`

        let error = false
        let buffer = Buffer.alloc(0)
        this.log(message)

        const script = spawn(cmd.command, cmd.args)

        script.stdout.on('data', (data) => {
          buffer = Buffer.concat([buffer, data])
        })

        script.stderr.on('data', (data) => {
          buffer = Buffer.concat([buffer, data])
          error = true
        })

        script.on('close', (code) => {
          this.log(`${message} exit code: ${code}`)
          if (error) {
            error = new Error(buffer.toString())
            reject(error)
          }
          resolve()
        })
      })
    })
    return Promise.all(promises)
  }

  createFlash () {
    const os = this.store.get('os')
    const result = { message: `${this.flash.command} ${this.flash.args.join(' ')}` }

    if (os === 'linux' || os === 'darwin') {
      const options = { name: 'KruxInstaller' }
      const sudoer = new Sudoer(options)
      result.spawn = async () => {
        return await sudoer.spawn(result.message)
      }
    } else if (os === 'win32') {
      result.spawn = () => {
        return new Promise((resolve) => {
          resolve(spawn(this.flash.command, this.flash.args))
        })
      }
    } else {
      throw new Error(`${os} not implemented`)
    }
    return result
  }

  async write () {
    const flash = this.createFlash()
    const message = flash.message
    const runner = await flash.spawn()

    runner.stdout.on('data', (data) => {
      const out = Buffer.from(data, 'utf-8').toString()
      this.log(out)
      this.send(`${this.name}:data`, out)
    })

    runner.stderr.on('data', (data) => {
      const out = Buffer.from(data, 'utf-8').toString()
      this.log(out)
      this.send(`${this.name}:data`, out)
    })

    runner.on('close', (code) => {
      this.log(`${message} exit code: ${code}`)
      this.send(`${this.name}:success`)
    })
  }
}

/**
 * Function to handle the
 * Flashing (write krux firmware direct onto device) process
 *
 * @param win
 * @param store
 */
export default function (win, store) {
  // eslint-disable-next-line no-unused-vars
  return async function (_event, options) {
    const handler = new FlashHandler(win, store)
    handler.setup()
    await handler.enable()
    await handler.write()
  }
}
