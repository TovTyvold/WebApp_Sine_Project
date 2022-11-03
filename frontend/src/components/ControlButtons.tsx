import { useState, useCallback } from 'react';

const ControllButtons = ({ saveProfile, restoreProfile, getFlow }: any) => {
  const [savedProfiles, setSavedProfiles] = useState<string[]>([]);
  const [showSaves, setShowSaves] = useState<boolean>(false);

  const getSavedProfiles = useCallback(() => {
    let arr: string[] = [];
    const keys = Object.keys(localStorage);
    for (let key of keys) {
      arr.push(key);
    }
    setSavedProfiles(arr);
  }, []);

  const onSave = useCallback(
    (event: any) => {
      event.preventDefault();

      saveProfile();
      getSavedProfiles();
    },
    [saveProfile, getSavedProfiles]
  );

  const openSaves = useCallback(
    (event: any) => {
      event.preventDefault();
      if (localStorage.length > 0) {
        getSavedProfiles();
        if (showSaves === false) {
          setShowSaves(true);
        } else {
          setShowSaves(false);
        }
      }
    },
    [showSaves]
  );

  const handleLoad = useCallback((event: any, profile: string) => {
    event.preventDefault();
    restoreProfile(profile);
    setShowSaves(false);
  }, []);

  return (
    <div
      style={{
        zIndex: 4,
        position: 'absolute',
        display: 'flex',
        width: '100%',
        marginRight: '1rem',
      }}>
      <div style={{ left: 0 }}>
        <button className='btn' onClick={openSaves}>
          Load
        </button>
        <button className='btn' onClick={onSave}>
          Save
        </button>
      </div>
      {showSaves && (
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          {savedProfiles.map((profile: string) => {
            return (
              <button
                className='btn-small'
                key={profile}
                value={profile}
                onClick={(e) => handleLoad(e, profile)}>
                {profile}
              </button>
            );
          })}
        </div>
      )}
      <div style={{ marginLeft: 'auto' }}>
        <button className='btn' onClick={getFlow}>
          Play
        </button>
      </div>
    </div>
  );
};
export default ControllButtons;
