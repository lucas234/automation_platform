import request from '@/utils/request'

export function getApiList(params) {
  return request({
    url: '/v1/apis/',
    method: 'get',
    params
  })
}

export function createApi(data) {
  return request({
    url: '/v1/api/',
    method: 'post',
    data
  })
}

export function updateApi(id, data) {
  return request({
    url: '/v1/apis/' + id,
    method: 'put',
    data
  })
}

export function deleteApi(id) {
  return request({
    url: '/v1/apis/' + id,
    method: 'delete'
  })
}
