import React, { useState } from "react";

export const useForm = (callback: any, initialState = {}) => {
    const [values, setValues] = useState(initialState);

    const onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setValues({...values, [event.target.name]: event.target.value})
    };

    const onSubmit = async (event: any) => {
        event.preventDefault();
        await callback();
    }

    return {
        onChange, onSubmit, values
    };


}