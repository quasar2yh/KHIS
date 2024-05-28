import React from 'react'
import { useSelector } from 'react-redux'
import { useParams } from 'react-router-dom'

function Department() {
    const params = useParams()
    const departmentList = useSelector(state => state.departmentReducer.departmentList)
    console.log("departmentList", departmentList)
    return (
        <div>Department</div>
    )
}

export default Department