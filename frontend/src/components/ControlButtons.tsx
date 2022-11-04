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
    [showSaves, getSavedProfiles]
  );

  const handleLoad = useCallback(
    (event: any, profile: string) => {
      event.preventDefault();
      restoreProfile(profile);
      setShowSaves(false);
    },
    [restoreProfile]
  );

  return (
    <div
      style={{
        zIndex: 4,
        position: 'absolute',
        display: 'flex',
        width: '100%',
        marginRight: '1rem',
      }}>
      <button className='btn' onClick={onSave}>
        Save
      </button>
      <button className='btn' onClick={openSaves}>
        Load
      </button>

      {showSaves && (
        <div
          style={{
            display: 'flex',
            height: '30px',
            marginTop: '1rem',
          }}>
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
