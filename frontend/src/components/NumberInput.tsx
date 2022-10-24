//import TextField from '@mui/material/Textfield';
export default function NumberInput({
  label,
  name,
  value,
  // index,
  onChange,
}: any): JSX.Element {
  return (
    // <TextField
    //   variant='outlined'
    //   label={label}
    //   type='number'
    //   name={name}
    //   placeholder={label}
    //   value={value}
    //   onChange={(event) => onChange(index, event)}
    // />
    <label className='osc-input'>
      {label}
      <input
        type='number'
        step='any'
        min={0}
        name={name}
        placeholder={label}
        value={value}
        // onChange={(event) => onChange(index, event)}
        onChange={onChange}
      />
    </label>
  );
}
