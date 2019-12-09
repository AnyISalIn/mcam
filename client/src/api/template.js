import request from '@/utils/request'

export function listTemplate() {
  return request({
    url: '/templates',
    method: 'get'
  })
}

export function updateTemplate(id, data) {
  return request({
    url: `/templates/${id}`,
    method: 'patch',
    data
  })
}

export function detailTemplate(id) {
  return request({
    url: `/templates/${id}`,
    method: 'get'
  })
}

export function createTemplate(data) {
  return request({
    url: `/templates`,
    method: 'post',
    data
  })
}

export function destroyTemplate(id) {
  return request({
    url: `/templates/${id}`,
    method: 'delete'
  })
}
