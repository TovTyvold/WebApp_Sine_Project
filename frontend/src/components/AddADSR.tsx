import { useEffect, useState } from "react";

type Adsr = {
    attack: number;
    decay: number;
    sustain: number;
    release: number;
};

const defaultAdsr: Adsr = {
    attack: 1,
    decay: 1,
    sustain: 3,
    release: 1,
};

export default function AddADSR(props: any) {

    const [adrs, setAdsr] = useState<Adsr[]>([defaultAdsr]);

    const handleInputChange = (
        index: number,
        e: React.ChangeEvent<HTMLInputElement>
      ) => {
        const { name, value } = e.currentTarget;
        let val: any = value;
        const list: any[] = [...adrs];
        list[index][name] = val;
        setAdsr(list);
    };

    return (
        <div style={{ float:"right" }}>
            {adrs.map((element, index) => {
                return (
                    <div key={index}>
                            <input
                            type='number'
                            name='attack'
                            placeholder='Attack'
                            value={element.attack}
                            onChange={(event) => handleInputChange(index, event)}
                            />
                            <input
                            type='number'
                            name='decay'
                            placeholder='Decay'
                            value={element.decay}
                            onChange={(event) => handleInputChange(index, event)}
                            />
                            <input
                            type='text'
                            name='sustain'
                            placeholder='Sustain'
                            value={element.sustain}
                            onChange={(event) => handleInputChange(index, event)}
                            />
                            <input
                            type='text'
                            name='release'
                            placeholder='Release'
                            value={element.release}
                            onChange={(event) => handleInputChange(index, event)}
                            />
                    </div>
                    );
                })}
        </div>
    );
  }