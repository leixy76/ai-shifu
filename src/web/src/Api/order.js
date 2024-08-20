import request from "../Service/Request";

export const testPurchaseOrder = ({ orderId }) => {
  return request({
    url: '/api/order/order-test',
    method: 'post',
    data: { order_id: orderId }
  });
}

// 创建订单
export const initOrder = () => {
  return request({
    url: '/api/order/init-order',
    method: 'post',
    data: { course_id: process.env.REACT_APP_COURSE_ID }
  });
}

// 获取支付链接
export const getPayUrl = ({ channel, orderId }) => {
  return request({
    method: 'POST',
    url: '/api/order/reqiure-to-pay',
    data: { channel, order_id: orderId }
  });
}

// 查询订单
export const queryOrder = ({ orderId }) => {
  return request({
    method: 'POST',
    url: '/api/order/query-order',
    data: { order_id: orderId },
  });
}

// 使用优惠码
export const applyDiscountCode = ({ orderId, code }) => {
  return request({
    method: 'POST',
    url: '/api/order/apply-discount',
    data: {
      discount_code: code,
      order_id: orderId,
    }
  });
}
