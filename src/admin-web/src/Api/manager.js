import request from '../Service/Request';


export const getViewInfo = async (view_name) => {
    return request({
        url: '/api/manager/view-info',
        method: 'post',
        data: { view_name },
    });
    }

export const queryView = async (view_name, page,page_size,query) => {
    return request({
        url: '/api/manager/query-view',
        method: 'post',
        data: { view_name, page, page_size, query },
    });
    }