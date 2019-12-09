import request from '@/utils/request'

export function createInstance(data) {
  return request({
    url: '/instances',
    method: 'post',
    data
  })
}

export function listInstance() {
  return request({
    url: '/instances',
    method: 'get'
  })
}

export function destroyInstance(instance_id) {
  return request({
    url: `/instances/${instance_id}`,
    method: 'delete'
  })
}

export function InstanceAction(instance_id, params) {
  return request({
    url: `/instances/${instance_id}`,
    method: 'post',
    params: params
  })
}

export function detailInstance(instance_id) {
  return request({
    url: `/instances/${instance_id}`,
    method: 'get'
  })
}

export function updateInstance(instance_id, data) {
  return request({
    url: `/instances/${instance_id}`,
    method: 'patch',
    data
  })
}
