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
          border: 'solid 1px #1f939e',
          borderRadius: '5px',
          backgroundColor: 'white',
          padding: '10px',
        }}>
        <b> Add Node</b>
        <hr />
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <button onClick={() => onClick('oscillator')}>Oscillator </button>
          <button onClick={() => onClick('envelope')}>Envelope </button>
          <button onClick={() => onClick('effect')}>Effect </button>
          <button onClick={() => onClick('operation')}>Operation </button>
          <button onClick={() => onClick('value')}>Value </button>
          <button onClick={() => onClick('bezier')}>Bezier </button>
        </div>
      </div>
    ) : null;
  }
);
