import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import Cookies from 'js-cookie';
import { getUserIdAction, getAccountInfoAction } from '../redux/modules/userActions';

const TokenRefresher = ({ children }) => {
    const dispatch = useDispatch();
    const userId = useSelector((state) => state.userReducer.userId);
    const access = Cookies.get('access');

    useEffect(() => {
        // 액세스 토큰이 있는 경우 userId, AccountInfo 세팅
        if (access) {
            dispatch(getUserIdAction(access));
            dispatch(getAccountInfoAction(userId));
        }
    }, [dispatch, access, userId]);

    return <>{children}</>;
};

export default TokenRefresher;
