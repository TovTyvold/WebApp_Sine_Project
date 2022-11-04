import { memo, useState, useEffect } from 'react';

export const ContextMenu = memo(
  ({ show, position, onClick }: any): JSX.Element | null => {
    const [searchTerm, setSearchTerm] = useState('');
    const options = [
      'oscillator',
      'envelope',
      'effect',
      'operation',
      'value',
      'bezier',
      'mix',
    ];

    useEffect(() => {}, [searchTerm]);

    useEffect(() => {
      if (!show) setSearchTerm('');
    }, [show]);

    return show ? (
      <div
        style={{
          position: 'absolute',
          top: position.y,
          left: position.x,
          zIndex: 100,
          border: 'solid 1px #1f939e',
          borderRadius: '5px',
          backgroundColor: 'white',
          padding: '10px',
        }}>
        <b> Add Node</b>
        <br />
        <input
          type='text'
          placeholder='Search'
          autoFocus
          onChange={(event: any) => {
            setSearchTerm(event.target.value);
          }}
        />
        <hr />
        <div style={{ display: 'flex', flexDirection: 'column' }} id='ctxMenu'>
          {options
            .filter((option) => {
              if (searchTerm === '') {
                return option;
              } else if (option.includes(searchTerm.toLocaleLowerCase())) {
                return option;
              } else {
                return null;
              }
            })
            .map((option) => {
              return (
                <button
                  key={option}
                  className='btn-small'
                  onClick={() => onClick(option)}>
                  {option.charAt(0).toUpperCase() + option.slice(1)}
                </button>
              );
            })}
        </div>
      </div>
    ) : null;
  }
);
