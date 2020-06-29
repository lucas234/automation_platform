import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/v1/login',
    method: 'post',
    data // { 'username': 'lucas9', 'password': '1234' }
  })
}

export function getInfo() {
  return request({
    url: 'v1/users/2',
    method: 'get'
    // params: { token }
  })
}

export function logout() {
  return request({
    url: '/v1/login',
    method: 'post',
    data: { 'username': 'lucas9', 'password': '12342222' }
  })
}


