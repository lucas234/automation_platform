import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/v1/apis/',
    method: 'get',
    params
  })
}
