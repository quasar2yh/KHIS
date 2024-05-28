import { combineReducers, createStore, applyMiddleware } from 'redux';
import userReducer from '../modules/user';
import { thunk } from 'redux-thunk';
import promiseMiddleware from "redux-promise";

const rootReducer = combineReducers({
    userReducer,
});

const store = createStore(rootReducer, applyMiddleware(thunk, promiseMiddleware))

export { rootReducer, store };
