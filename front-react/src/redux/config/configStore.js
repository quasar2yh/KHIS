import { combineReducers, createStore, applyMiddleware } from 'redux';
import userReducer from '../modules/user';
import { thunk } from 'redux-thunk';
import promiseMiddleware from "redux-promise";
import departmentReducer from '../modules/department';

const rootReducer = combineReducers({
    userReducer,
    departmentReducer
});

const store = createStore(rootReducer, applyMiddleware(thunk, promiseMiddleware))

export { rootReducer, store };
