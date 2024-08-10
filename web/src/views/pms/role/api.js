/**********************************
 * @Author: Ronnie Zhang
 * @LastEditor: Ronnie Zhang
 * @LastEditTime: 2023/12/05 21:29:27
 * @Email: zclzone@outlook.com
 * Copyright © 2023 Ronnie Zhang(大脸怪) | https://isme.top
 **********************************/

import { request } from '@/utils'

export default {
  create: (data) => request.post('/roles/', data),
  read: (params = {}) => request.get('/roles/', { params }),
  update: (data) => request.patch(`/roles/${data.id}/`, data),
  delete: (id) => request.delete(`/roles/${id}/`),

  getAllPermissionTree: () => request.get('/permissions/base/tree/'),
  getAllUsers: (params = {}) => request.get('/users/', { params }),
  addRoleUsers: (data) => request.post(`/role/users/`, data),
  removeRoleUsers: (roleId, data) => request.patch(`/roles/users/remove/${roleId}`, data),
}
