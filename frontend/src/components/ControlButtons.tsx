const ControllButtons = ({ getFlow }: any) => {
  return (
    <div style={{ zIndex: 4, position: 'absolute', display: 'flex', right: 0 }}>
      <div style={{ marginRight: '1rem' }}>
        <button className='btn' onClick={getFlow}>
          Play
        </button>
      </div>
    </div>
  );
};
export default ControllButtons;
