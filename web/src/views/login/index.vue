<!--------------------------------
 - @Author: Ronnie Zhang
 - @LastEditor: Ronnie Zhang
 - @LastEditTime: 2023/12/05 21:28:36
 - @Email: zclzone@outlook.com
 - Copyright © 2023 Ronnie Zhang(大脸怪) | https://isme.top
 --------------------------------->

<template>
  <div class="wh-full flex-col bg-[url(@/assets/images/login_bg.webp)] bg-cover">
    <div
      class="m-auto max-w-700 min-w-345 f-c-c rounded-8 bg-opacity-20 bg-cover p-12 card-shadow auto-bg"
    >
      <div class="hidden w-380 px-20 py-35 md:block">
        <img src="@/assets/images/login_banner.webp" class="w-full" alt="login_banner" />
      </div>

      <div class="w-320 flex-col px-20 py-32">
        <h2 class="f-c-c text-24 text-#6a6a6a font-normal">
          <img src="@/assets/images/logo.png" class="mr-12 h-50" />
          {{ title }}
        </h2>

        <!-- Add tabs for login and register -->
        <n-tabs v-model:value="activeTab" class="mt-20">
          <n-tab-pane name="login" tab="登录">
            <!-- Existing login form -->
            <n-input
              v-model:value="loginInfo.username"
              autofocus
              class="mt-32 h-40 items-center"
              placeholder="请输入用户名"
              :maxlength="50"
            >
              <template #prefix>
                <i class="i-fe:user mr-12 opacity-20" />
              </template>
            </n-input>
            <n-input
              v-model:value="loginInfo.password"
              class="mt-20 h-40 items-center"
              type="password"
              show-password-on="mousedown"
              placeholder="请输入密码"
              :maxlength="20"
              @keydown.enter="handleLogin()"
            >
              <template #prefix>
                <i class="i-fe:lock mr-12 opacity-20" />
              </template>
            </n-input>

            <n-checkbox
              class="mt-20"
              :checked="isRemember"
              label="记住我"
              :on-update:checked="(val) => (isRemember = val)"
            />

            <div class="mt-20 flex items-center">
              <n-button
                class="h-40 flex-1 rounded-5 text-16"
                type="primary"
                :loading="loading"
                @click="handleLogin()"
              >
                登录
              </n-button>
            </div>
          </n-tab-pane>
          <n-tab-pane name="register" tab="注册">
            <!-- Add register form here -->
            <n-input
              v-model:value="registerInfo.username"
              class="mt-32 h-40 items-center"
              placeholder="请输入用户名"
              :maxlength="50"
            >
              <template #prefix>
                <i class="i-fe:user mr-12 opacity-20" />
              </template>
            </n-input>
            <n-input
              v-model:value="registerInfo.password"
              class="mt-20 h-40 items-center"
              type="password"
              show-password-on="mousedown"
              placeholder="请输入密码"
              :maxlength="20"
            >
              <template #prefix>
                <i class="i-fe:lock mr-12 opacity-20" />
              </template>
            </n-input>
            <n-input
              v-model:value="registerInfo.confirmPassword"
              class="mt-20 h-40 items-center"
              type="password"
              show-password-on="mousedown"
              placeholder="请确认密码"
              :maxlength="20"
            >
              <template #prefix>
                <i class="i-fe:lock mr-12 opacity-20" />
              </template>
            </n-input>
            <div class="mt-20 flex items-center">
              <n-button
                class="h-40 flex-1 rounded-5 text-16"
                type="primary"
                :loading="loading"
                @click="handleRegister()"
              >
                注册
              </n-button>
            </div>
          </n-tab-pane>
        </n-tabs>
      </div>
    </div>

    <TheFooter class="py-12" />
  </div>
</template>

<script setup>
import { throttle, lStorage } from '@/utils'
import { useStorage } from '@vueuse/core'
import api from './api'
import { useAuthStore } from '@/store'
import { ref } from 'vue'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const title = import.meta.env.VITE_TITLE

const loginInfo = ref({
  username: '',
  password: '',
})

const localLoginInfo = lStorage.get('loginInfo')
if (localLoginInfo) {
  loginInfo.value.username = localLoginInfo.username || ''
  loginInfo.value.password = localLoginInfo.password || ''
}

const isRemember = useStorage('isRemember', true)
const loading = ref(false)
const activeTab = ref('login')

const registerInfo = ref({
  username: '',
  password: '',
  confirmPassword: '',
})

async function handleLogin(isQuick) {
  const { username, password, captcha } = loginInfo.value
  if (!username || !password) return $message.warning('请输入用户名和密码')
  try {
    loading.value = true
    $message.loading('正在验证，请稍后...', { key: 'login' })
    const { data } = await api.login({ username, password: password.toString(), captcha, isQuick })
    if (isRemember.value) {
      lStorage.set('loginInfo', { username, password })
    } else {
      lStorage.remove('loginInfo')
    }
    await onLoginSuccess(data)
  } catch (error) {
    console.log('login error')
    // 10003为验证码错误专属业务码
    //if (error?.code === 10003) {
      // 为防止爆破，验证码错误则刷新验证码
      //initCaptcha()
    //}
    $message.destroy('login')
    console.error(error)
  }
  loading.value = false
}

async function onLoginSuccess(data = {}) {
  authStore.setToken({ accessToken: data.access})
  $message.loading('登录中...', { key: 'login' })
  try {
    $message.success('登录成功', { key: 'login' })
    if (route.query.redirect) {
      const path = route.query.redirect
      delete route.query.redirect
      router.push({ path, query: route.query })
    } else {
      router.push('/')
    }
  } catch (error) {
    console.error(error)
    $message.destroy('login')
  }
}

async function onRegisterSuccess(data = {}) {
  authStore.setToken({ accessToken: data.access })
  $message.loading('注册成功，正在登录...', { key: 'register' })
  try {
    $message.success('登录成功', { key: 'register' })
    if (route.query.redirect) {
      const path = route.query.redirect
      delete route.query.redirect
      router.push({ path, query: route.query })
    } else {
      router.push('/')
    }
  } catch (error) {
    console.error(error)
    $message.destroy('register')
  }
}

async function handleRegister() {
  const { username, password, confirmPassword } = registerInfo.value
  if (!username || !password || !confirmPassword) {
    return $message.warning('请填写所有注册信息')
  }
  if (password !== confirmPassword) {
    return $message.warning('两次输入的密码不一致')
  }
  // add password length check
  if (password.length < 6) {
    return $message.warning('密码长度不能小于6位')
  }
  // Implement registration logic here
  try {
    loading.value = true
    $message.loading('正在注册，请稍后...', { key: 'register' })
    // Call registration API
    const { data } = await api.register({ username, password })
    // Handle successful registration
    await onRegisterSuccess(data)
    $message.success('注册成功', { key: 'register' })
    activeTab.value = 'login' // Switch to login tab after successful registration
  } catch (error) {
    console.error(error)
    $message.error('注册失败，请重试', { key: 'register' })
  } finally {
    loading.value = false
  }
}
</script>
