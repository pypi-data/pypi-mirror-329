import React from 'react';
import { Form } from 'react-bootstrap';
import { ALGO_INPUT_FIELDS } from '../constants';
import { BsFillXCircleFill } from 'react-icons/bs';
import TextField from '@mui/material/TextField';
import Switch from '@mui/material/Switch';
import TableCell from '@mui/material/TableCell';
import TableRow from '@mui/material/TableRow';

export const InputRow = ({row, handleRemoveRow, handleDataChange }) => {
    return (
        <TableRow id={row.inputId.toString()}>
            <TableCell> </TableCell>
            <TableCell>
                <TextField
                    id={ALGO_INPUT_FIELDS.INPUT_NAME}
                    placeholder="What is the input name?"
                    size="small"
                    onChange={handleDataChange}
                    value={row.inputName}
                    sx={{width: '35ch'}}/>
            </TableCell>
            <TableCell>
                <TextField
                    id={ALGO_INPUT_FIELDS.INPUT_DESC}
                    placeholder="Describe the input parameter"
                    size="small" 
                    onChange={handleDataChange}
                    value={row.inputDesc}
                    sx={{width: '35ch'}}/>
            </TableCell>
            <TableCell>
                <Switch
                    id={ALGO_INPUT_FIELDS.IS_REQUIRED}
                    name="required"
                    onChange={handleDataChange}
                    checked={row.isRequired}/>
            </TableCell>
            <TableCell>
                <TextField
                    id={ALGO_INPUT_FIELDS.INPUT_DEFAULT}
                    placeholder="Default value"
                    size="small" 
                    onChange={handleDataChange}
                    value={row.inputDefault}
                    sx={{width: '25ch'}}/>
            </TableCell>
            <TableCell>
                <BsFillXCircleFill className="danger-icon" id={row.inputId.toString()} onClick={() => handleRemoveRow(row.inputId.toString())}/>
            </TableCell>
        </TableRow>
    )
}