import React, { useEffect, useState } from 'react';
import { OverlayTrigger, Row, Tooltip } from 'react-bootstrap';
import { BsPlusCircleFill, BsInfoCircle, BsFillInfoCircleFill } from 'react-icons/bs';
import { useDispatch, useSelector } from 'react-redux';
import { algorithmActions, selectAlgorithm } from '../redux/slices/algorithmSlice'
import { ALGO_INPUTS, ALGO_INPUTS_DESC, ALGO_INPUT_FIELDS } from '../constants';
import { InputRow } from './InputRow';
import { EmptyRow } from './EmptyRow';
import { Tooltip as ReactTooltip } from "react-tooltip";
import Table from '@mui/material/Table';
import TableContainer from '@mui/material/TableContainer';
import Paper from '@mui/material/Paper';
import TableBody from '@mui/material/TableBody';
import TableRow from '@mui/material/TableRow';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';

export const TablePositionalInputs = () => {

    // Redux
    const dispatch = useDispatch()

    const { positionalData, inputId } = useSelector(selectAlgorithm)
    const { addPositionalData, updatePositionalData, removePositionalData, incrementInputId } = algorithmActions

    const addRow = () => {
        dispatch(addPositionalData({[ALGO_INPUT_FIELDS.INPUT_NAME]: "", 
                                    [ALGO_INPUT_FIELDS.INPUT_DEFAULT]: "", 
                                    [ALGO_INPUT_FIELDS.INPUT_DESC]: "", 
                                    [ALGO_INPUT_FIELDS.IS_REQUIRED]: false, 
                                    [ALGO_INPUT_FIELDS.INPUT_ID]: inputId }))
        dispatch(incrementInputId())
    }

    const handleDataChange = e => {
        switch (e.target.type) {
            case "checkbox": {
                dispatch(updatePositionalData({inputId: e.target.parentNode.parentNode.parentNode.parentNode.id, inputField: [e.target.id], inputValue: e.target.checked}))
                break;
            }
            default: dispatch(updatePositionalData({inputId: e.target.parentNode.parentNode.parentNode.parentNode.id, inputField: [e.target.id], inputValue: e.target.value}))
            break;
        }
    }

    const handleRemoveRow = (inputId) => {
        dispatch(removePositionalData({key: inputId}))
    }

    return (
        <div>
            <div className="input-types">
                <h4>Positional Inputs</h4>
                <ReactTooltip
                    anchorId="positional_input_info"
                    place="right"
                    variant="dark"
                    content={ALGO_INPUTS_DESC.POSITIONAL_INPUTS}
                />
                <span id="positional_input_info"><BsInfoCircle /></span>
            </div>
            <div style={{ display: 'flex', alignItems: 'left' }}>
                <TableContainer component={Paper}>
                    <Table aria-label="simple table" sx={{ border: 'none' }}>
                        <TableHead>
                            <TableRow>
                                <TableCell align="left"><BsPlusCircleFill className="success-icon" onClick={addRow} /></TableCell>
                                <TableCell align="left" sx={{ fontSize: '16px' }}>Name</TableCell>
                                <TableCell align="left" sx={{ fontSize: '16px' }}>Description</TableCell>
                                <TableCell align="left" sx={{ fontSize: '16px' }}>Required?</TableCell>
                                <TableCell align="left" sx={{ fontSize: '16px' }}>Default Value</TableCell>
                                <TableCell></TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {positionalData.length == 0 ? <TableRow><TableCell colSpan={6} align="center" className="empty-row" sx={{ fontSize: '16px' }}>No inputs specified</TableCell></TableRow> : Object.entries(positionalData).map(([key, data]) => {
                                return <InputRow row={data} handleRemoveRow={handleRemoveRow} handleDataChange={handleDataChange}/>
                            })}
                        </TableBody>
                    </Table>
                </TableContainer>
            </div>
        </div>
    )
}