import request from '@/utils/request'

export function listProvider() {
  return request({
    url: '/providers',
    method: 'get'
  })
}

export function createProvider(data) {
  return request({
    url: '/providers',
    method: 'post',
    data
  })
}

export function destroyProvider(provider_id) {
  return request({
    url: `/providers/${provider_id}`,
    method: 'delete'
  })
}

export function updateProvider(provider_id, data) {
  return request({
    url: `/providers/${provider_id}`,
    method: 'patch',
    data: data
  })
}
