/**********************************
 * @Author: Ronnie Zhang
 * @LastEditor: Ronnie Zhang
 * @LastEditTime: 2023/12/05 21:31:02
 * @Email: zclzone@outlook.com
 * Copyright © 2023 Ronnie Zhang(大脸怪) | https://isme.top
 **********************************/

import path from 'path'
import { defineConfig, loadEnv } from 'vite'
import { execSync } from 'child_process'
import Vue from '@vitejs/plugin-vue'
import Unocss from 'unocss/vite'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { NaiveUiResolver } from 'unplugin-vue-components/resolvers'
import simpleHtmlPlugin from 'vite-plugin-simple-html'
import removeNoMatch from 'vite-plugin-router-warn'
import svgLoader from 'vite-svg-loader';
import { pluginPagePathes, pluginIcons } from './build/plugin-isme'

// Get the current Git commit hash
const getGitCommitHash = () => {
  try {
    return execSync('git rev-parse --short HEAD').toString().trim()
  } catch (error) {
    console.error('Failed to get Git commit hash:', error)
    return 'unknown'
  }
}

export default defineConfig(({ command, mode }) => {
  const isBuild = command === 'build'
  const viteEnv = loadEnv(mode, process.cwd())
  const { VITE_TITLE, VITE_PUBLIC_PATH, VITE_PROXY_TARGET, VITE_PROXY_TARGET_MEDIA } = viteEnv
  const commitHash = getGitCommitHash()
  
  console.log('Current Git commit hash:', commitHash)
  console.log('Vite configuration mode:', mode)
  console.log('VITE_PROXY_TARGET:', VITE_PROXY_TARGET)

  return {
    base: VITE_PUBLIC_PATH || '/',
    plugins: [
      Vue(),
      svgLoader(),
      Unocss(),
      AutoImport({
        imports: ['vue', 'vue-router'],
        dts: false,
      }),
      Components({
        resolvers: [NaiveUiResolver()],
        dts: false,
      }),
      simpleHtmlPlugin({
        minify: isBuild,
        inject: {
          data: {
            title: VITE_TITLE,
          },
        },
      }),
      // 自定义插件，用于生成页面文件的path，并添加到虚拟模块
      pluginPagePathes(),
      // 自定义插件，用于生成自定义icon，并添加到虚拟模块
      pluginIcons(),
      // 移除非必要的vue-router动态路由警告: No match found for location with path
      removeNoMatch(),
    ],
    resolve: {
      alias: {
        '@': path.resolve(process.cwd(), 'src'),
        '~': path.resolve(process.cwd()),
      },
    },
    server: {
      host: '0.0.0.0',
      port: 3200,
      open: false,
      proxy: {
        '/api': {
          target: VITE_PROXY_TARGET,
          changeOrigin: true,
          rewrite: (path) => path.replace(new RegExp('^/api'), ''),
          secure: false,
          configure: (proxy, options) => {
            // 配置此项可在响应头中看到请求的真实地址
            proxy.on('proxyRes', (proxyRes, req) => {
              proxyRes.headers['x-real-url'] = new URL(req.url || '', options.target)?.href || ''
            })
          },
        },
        '/media': {
          target: VITE_PROXY_TARGET_MEDIA,
          changeOrigin: true,
          secure: false,
        }
      },
    },
    preview: {
      host: '0.0.0.0',
      port: 3200,
      open: false,
      proxy: {
        '/api': {
          target: VITE_PROXY_TARGET,
          changeOrigin: true,
          rewrite: (path) => path.replace(new RegExp('^/api'), ''),
          secure: false,
          configure: (proxy, options) => {
            // 配置此项可在响应头中看到请求的真实地址
            proxy.on('proxyRes', (proxyRes, req) => {
              proxyRes.headers['x-real-url'] = new URL(req.url || '', options.target)?.href || ''
            })
          },
        },
        '/media': {
          target: VITE_PROXY_TARGET_MEDIA,
          changeOrigin: true,
          secure: false,
        }
      },
    },
    build: {
      chunkSizeWarningLimit: 1024, // chunk 大小警告的限制（单位kb）
    },
    define: {
      __COMMIT_HASH__: JSON.stringify(commitHash),
    },
  }
})
