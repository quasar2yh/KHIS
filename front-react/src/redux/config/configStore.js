import { combineReducers, createStore, applyMiddleware } from 'redux';
import user from '../modules/user';
import { thunk } from 'redux-thunk';
import promiseMiddleware from "redux-promise";

const rootReducer = combineReducers({
    user
});

const store = createStore(rootReducer, applyMiddleware(thunk, promiseMiddleware))

export { rootReducer, store };
