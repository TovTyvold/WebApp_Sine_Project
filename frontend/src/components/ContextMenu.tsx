import { memo } from 'react';

export const ContextMenu = memo(
  ({ show, position, onClick }: any): JSX.Element | null => {
    return show ? (
      <div
        style={{
          position: 'absolute',
          top: position.y,
          left: position.x,
          zIndex: 100,
          border: 'solid 1px blue',
          backgroundColor: 'white',
          padding: '10px',
          display: 'flex',
          flexDirection: 'column',
        }}>
        Menu
        <br />

        <ul style={{ display: "flex", flexDirection: "column" }}>
          <label onClick={() => onClick("oscillator")}> Add Oscillator </label>
          <label onClick={() => onClick("envelope")}> Add Envelope </label>
          <label onClick={() => onClick("effect")}> Add Effect </label>
          <label onClick={() => onClick("operation")}> Add Operation </label>
        </ul>


      </div>
    ) : null;
  }
);
