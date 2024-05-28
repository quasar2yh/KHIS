import { getDepartments } from "../../apis/apis";

export const getDepartmentListAction = () => {
    const departmentList = getDepartments();
    return {
        type: 'SET_DEPARTMENT_LIST',
        payload: departmentList
    };
};