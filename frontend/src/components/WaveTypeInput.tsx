import React, { useState } from "react";

export default function WaveTypeInput() {
  const options: any = ["sin", "square", "saw", "triangle"];
  const [type, setType] = useState("");
  const handleSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setType(e.target.value);
  };
  return (
    <>
      <select value={type} onChange={handleSelect}>
        {options.map((option: string) => {
          <option value={option}>{option}</option>;
        })}
      </select>
    </>
  );
}
