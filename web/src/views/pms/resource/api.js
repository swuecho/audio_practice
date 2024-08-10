/**********************************
 * @Author: Ronnie Zhang
 * @LastEditor: Ronnie Zhang
 * @LastEditTime: 2024/04/01 15:52:04
 * @Email: zclzone@outlook.com
 * Copyright © 2023 Ronnie Zhang(大脸怪) | https://isme.top
 **********************************/

import axios from 'axios'
import { request } from '@/utils'

export default {
  getMenuTree: () => request.get('/permissions/menu/tree/'),
  getButtons: ({ parent_id }) => request.get(`/permissions/button/${parent_id}/`),
  getComponents: () => axios.get(`${import.meta.env.VITE_PUBLIC_PATH}components.json`),
  addPermission: (data) => request.post('/permissions/', data),
  savePermission: (id, data) => request.patch(`/permissions/${id}/`, data),
  deletePermission: (id) => request.delete(`permissions/${id}/`),
}
