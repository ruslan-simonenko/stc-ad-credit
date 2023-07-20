import type {App, Plugin} from 'vue'
import {inject} from "vue";

import axios, {AxiosInstance} from "axios";

interface Options {
  baseUrl?: string
}

const apiClientAxiosKey = Symbol('apiClientAxios')

export const useApiClientAxios: () => AxiosInstance = () => inject(apiClientAxiosKey)!

// noinspection JSUnusedGlobalSymbols
export const ApiClientAxios: Plugin = {
  install: (app: App, _options: Options) => {
    const apiClientAxios = axios.create({
      baseURL: "/api",
    })
    app.provide(apiClientAxiosKey, apiClientAxios)
  }
}
