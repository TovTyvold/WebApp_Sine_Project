import { memo } from 'react';

export const ContextMenu = memo(
  ({ show, position, options }: any): JSX.Element | null => {
    return show ? (
      <div
        style={{
          position: 'absolute',
          top: position.y - 350,
          left: position.x - 375,
          zIndex: 100,
          border: 'solid 1px blue',
          backgroundColor: 'white',
          padding: '10px',
          display: 'flex',
          flexDirection: 'column',
        }}>
        Menu
        <br />
        {options.map((option: any) => {
          <button key={option.label} onClick={option.effect}>
            {option.label}
          </button>;
        })}
      </div>
    ) : null;
  }
);
