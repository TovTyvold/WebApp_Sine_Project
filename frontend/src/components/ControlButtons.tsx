const ControllButtons = ({ getFlow }: any) => {
  return (
    <div style={{ zIndex: 4, position: 'absolute', display: 'flex' }}>
      <div style={{ marginRight: '1rem' }}>
        <button className='btn' onClick={getFlow}>
          Submit
        </button>
      </div>
    </div>
  );
};
export default ControllButtons;
