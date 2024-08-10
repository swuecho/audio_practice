/**********************************
 * @Author: Ronnie Zhang
 * @LastEditor: Ronnie Zhang
 * @LastEditTime: 2023/12/05 21:29:51
 * @Email: zclzone@outlook.com
 * Copyright © 2023 Ronnie Zhang(大脸怪) | https://isme.top
 **********************************/

import { request } from '@/utils'

export default {
  create: (data) => request.post('/users/', data),
  read: (params = {}) => request.get('/users/', { params }),
  update: (data) => request.post(`/user/roles/`, data),
  delete: (id) => request.delete(`/users/${id}`),
  getAllRoles: () => request.get('/roles/?enable=1'),
}
